import json
from typing import Iterator, List, Union

import pandas as pd
import requests
from loguru import logger
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pydantic import ValidationError
from streamlit.delta_generator import DeltaGenerator

from real_estate_tools.consts import PropertyDetails, ZP_Data


def properties_to_df(
    properties: Iterator[Union[None, PropertyDetails]]
) -> pd.DataFrame:
    """Generate a flat dataframe from an iterator of PropertyDetails's

    Parameters
    ----------
    properties : List[PropertyDetails]
        The properties to export

    Returns
    -------
    pd.DataFrame
        _description_
    """
    result = pd.DataFrame(
        map(lambda x: x.model_dump() if x is not None else None, properties)
    )
    return result


def area_to_sqft(value: Union[int, float], unit: str) -> Union[int, float]:
    unit = unit.lower()
    supported_area_units = [
        "square feet",
    ]
    if unit in supported_area_units:
        if unit == "square feet":
            return value
    logger.warning(
        f"Supported area units are: {supported_area_units}; {unit} is not one of them"
    )
    return 0


def raw_zillow_to_property_details(raw_data: dict) -> PropertyDetails:
    return PropertyDetails(
        address=f'{raw_data["streetAddress"]}, {raw_data["city"]}',
        full_address=(
            f"{raw_data['streetAddress']}, {raw_data['city']},"
            f" {raw_data['state']} {raw_data['zipcode']}"
        ),
        lat=raw_data["latitude"],
        lon=raw_data["longitude"],
        link=f"https://www.zillow.com{raw_data['hdpUrl']}",
        # home_status=raw_data["homeStatus"]
        thumbnail_link=raw_data["photos"][0]["mixedSources"]["webp"][0]["url"],
        parcel_id=raw_data["resoFacts"]["parcelNumber"],
        county=raw_data["county"],
        rooms=raw_data["bedrooms"],
        baths=raw_data["bathrooms"],
        built_year=raw_data["yearBuilt"],
        listed_price=raw_data["price"],
        listed_date=raw_data["priceHistory"][0]["date"],
        garages=raw_data["resoFacts"]["parkingCapacity"],
        living_area=raw_data["livingArea"] if raw_data["livingArea"] else 0,
        lot_area=area_to_sqft(unit=raw_data["lotAreaUnits"], value=raw_data["lotSize"]),
    )


def clean_zpid(zpid: str) -> str:
    return zpid.split("_")[0]


def get_property_detail(
    api_key: str, zpid: str
) -> requests.Response:  # pragma: no cover
    url = "https://app.scrapeak.com/v1/scrapers/zillow/property"
    querystring = {"api_key": api_key, "zpid": zpid}
    return requests.request("GET", url, params=querystring)


def fetch_properties(api_key: str, zpids: List[int]) -> List[ZP_Data]:
    results = []
    for zpid in zpids:
        tmp_res = get_property_detail(api_key, zpid).json()
        if not tmp_res["is_success"]:
            logger.warning("Something went wrong")
            logger.warning(f"Message is: {tmp_res['message']}")
        else:
            results.append(ZP_Data(**tmp_res["data"]))

    return results


def summarize_flip_calc(
    workbook: Workbook,
    general: pd.DataFrame,
    purchase_sell_cost_factors: pd.DataFrame,
    holding_costs: pd.DataFrame,
    rehab_costs: float,
) -> Workbook:
    def append_df(df: pd.DataFrame):
        for row in dataframe_to_rows(df, index=False, header=True):
            flip_calc.append(row)

    logger.info("Preparing flip summary sheet in a workbook")
    FLIP_CALC_SHEET_NAME = "Flip Calculator"

    flip_calc = (
        workbook[FLIP_CALC_SHEET_NAME]
        if FLIP_CALC_SHEET_NAME in workbook.sheetnames
        else workbook.create_sheet(FLIP_CALC_SHEET_NAME)
    )

    flip_calc.append(["General information"])
    append_df(general)

    flip_calc.append(list())
    flip_calc.append(["Purchase and sell cost factors"])
    append_df(purchase_sell_cost_factors)

    flip_calc.append(list())
    flip_calc.append(["Holding costs"])
    append_df(holding_costs)

    flip_calc.append(list())
    flip_calc.append(["Rehab costs"])
    flip_calc.append(["Total rehab", rehab_costs])

    return workbook


def st_warn_validation_error(
    st: DeltaGenerator, e: ValidationError
) -> None:  # pragma: no cover
    e = json.loads(e.json())
    for issue in e:
        st.warning(f"Field {issue['loc']} has an issue of type {issue['type']}")
