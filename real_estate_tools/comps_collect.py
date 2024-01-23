import json
from datetime import date
from typing import List, Union

import pandas as pd
import pygsheets
import streamlit as st
from loguru import logger
from pydantic import ValidationError
from streamlit.delta_generator import DeltaGenerator

from real_estate_tools import geoutils
from real_estate_tools.consts import PropertyDetails, Settings
from real_estate_tools.utils import (
    clean_zpid,
    get_property_detail,
    properties_to_df,
    raw_zillow_to_property_details,
    st_warn_validation_error,
)

settings = Settings()


def prop_tab(container: DeltaGenerator) -> Union[PropertyDetails, None]:
    logger.debug("Starting prop_tab")
    address = container.text_input(
        label="Provide full address of the property you're interested in",
        value="1600 Pennsylvania Avenue Washington, D.C.",
    )
    parsed_address = geoutils.forward_search(address=address)
    full_address = parsed_address["display_name"]
    lat = parsed_address["lat"]
    lon = parsed_address["lon"]

    link = container.text_input(label="Link to the property", value=None)
    # This is to handle the case that the link is changed by the user and then
    # removed
    link = link if link != "" else None
    listed_date = container.date_input(
        label="When was the property listed for sale?",
        value=date.today(),
        max_value=date.today(),
    )
    listed_price = container.number_input(
        label="Listed price ($)", min_value=1, step=1000, value=100_000
    )
    lot_area = container.number_input(
        label="Lot size ($\mathrm{ft}^2$)", min_value=1, step=10
    )
    living_area = container.number_input(
        label="Living area ($\mathrm{ft}^2$)", min_value=1, step=10
    )
    rooms = container.number_input(label="Number of rooms", min_value=1, step=1)
    baths = container.number_input(label="Number of rooms", min_value=1.0, step=0.5)
    garages = container.number_input(label="Number of garages", min_value=1, step=1)
    built_year = container.number_input(
        label="Built year",
        min_value=1800,
        max_value=date.today().year,
        value=1970,
        step=5,
    )

    submitted = container.button(label="Ready!")

    if submitted:
        try:
            main_prop = PropertyDetails(
                address=address,
                full_address=full_address,
                lat=lat,
                lon=lon,
                baths=baths,
                rooms=rooms,
                living_area=living_area,
                lot_area=lot_area,
                garages=garages,
                built_year=built_year,
                listed_date=listed_date,
                listed_price=listed_price,
                link=link,
            )
            st.session_state["main_prop"] = main_prop
        except ValidationError as e:
            # Render content of errors and return None
            logger.warning("Unable to validate the property. Returning None")
            return st_warn_validation_error(container, e)
    logger.debug("Returning None main property")
    return None


def comps_tab(container: DeltaGenerator) -> Union[None, List[PropertyDetails]]:
    logger.debug("Starting comps tab")
    result = None
    zpids = list(
        map(
            clean_zpid,
            container.text_input("Provide a ZPIDs (separated with commas)").split(","),
        )
    )

    container.write(f"Following ZPIDs will be processed:\n{zpids}")
    raw_results = []
    demo_data_fetch = container.toggle("Demo mode", value=False)
    continue_condition = container.button("Fetch data")
    if continue_condition:
        with open("./resources/raw_results_formated.json", "r") as f:
            raw_results = json.load(f)
        if not demo_data_fetch:
            raw_results = []
            for zpid in zpids:
                response = get_property_detail(settings.scrapeak_api_key, zpid)
                if response.status_code == 200:
                    response = response.json()
                    if response["is_success"]:
                        raw_results.append(response["data"])
        result = list(map(raw_zillow_to_property_details, raw_results))
        st.session_state["comps"] = result
        container.write(f"Fetched {len(raw_results)} entries")

    logger.debug("Returning None from comps tab")
    return result


logger.info("Collect COMPs for property started")
prop, comps, comps_result = st.tabs(["Property", "Comps", "Summary"])

with st.sidebar:
    with open("./real_estate_tools/sidebar.md", "r") as f:
        st.write("".join(line for line in f))
comps_result.write("In this tab the results from the other two tabs are collected.")

prop_tab(prop)
if "main_prop" in st.session_state:
    logger.debug(f"The current state is: {st.session_state.main_prop}")
    prop.map(
        pd.DataFrame(
            [[
                st.session_state.main_prop.lat,
                st.session_state.main_prop.lon,
                "#884999",
            ]],
            columns=["lat", "lon", "color"],
        ),
        color="color",
        size=10,
    )

comps_details = comps_tab(comps)
logger.debug(f"comps_details type is {type(comps_details)}")

final_df = None
email_share = None
if "main_prop" in st.session_state and "comps" not in st.session_state:
    comps_result.write(properties_to_df([st.session_state.main_prop]))
if "main_prop" not in st.session_state and "comps" in st.session_state:
    comps_result.write(properties_to_df(st.session_state.comps))
if "main_prop" in st.session_state and "comps" in st.session_state:
    logger.debug("Main prop and comps are ready")
    final_df = pd.concat(
        [
            properties_to_df([st.session_state.main_prop]),
            properties_to_df(st.session_state.comps),
        ],
        axis=0,
    )
    geoutils.compute_distance_in_df(
        ref_lat=st.session_state.main_prop.lat,
        ref_lon=st.session_state.main_prop.lon,
        df=final_df,
        inplace=True,
    )
    comps_result.write(final_df)

    spreadsheet_name = comps_result.text_input(
        label="Spreadsheet name",
        value=st.session_state.main_prop.full_address,
        help=(
            "Provide a name for the spreadsheet. Using the full address is a good"
            " idea 💡"
        ),
    )
    email_share = comps_result.text_input(
        label="Enter email with whom you want to share the result",
        placeholder="my_email@realestate.com",
    )

if final_df is not None and email_share:
    comps_result.write("Everything is ready 🎉")
    continue_condition = comps_result.button(
        f"Finalize G-Sheet and share with {email_share}"
    )
    if continue_condition:
        with st.spinner(f"Preparing Google Sheet and sharing it with {email_share}"):
            gc = pygsheets.authorize(
                service_account_json=settings.get_google_credentials_as_json()
            )
            sh = gc.create(title=spreadsheet_name)
            wks = sh.add_worksheet("Comps Summary")
            sh.del_worksheet(sh.sheet1)
            wks.set_dataframe(final_df, start="A1")
            sh.share(email_share, role="writer")
