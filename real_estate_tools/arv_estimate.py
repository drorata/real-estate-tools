import pandas as pd
import requests
import streamlit as st
from loguru import logger

from real_estate_tools import consts

logger.info("ARV estimator started")


def get_property_detail(api_key, zpid):
    splitted = zpid.split('_')
    finalZPID = splitted[0]
    url = "https://app.scrapeak.com/v1/scrapers/zillow/property"
    querystring = {"api_key": api_key, "zpid": finalZPID}
    return requests.request("GET", url, params=querystring)


api_key = st.text_input("Provide API key", type="password")

zpids = st.text_input("Provide a ZPIDs (separated with commas)")
zpids = zpids.split(",")
st.write(f"Following ZPIDs will be processed:\n{zpids}")


continue_condition = st.button("Continue")
if continue_condition:
    results = []
    with st.spinner("Wait for it..."):
        for zpid in zpids:
            tmp_res = get_property_detail(api_key, zpid).json()
            if not tmp_res["is_success"]:
                logger.warning("Something went wrong")
                logger.warning(f"Message is: {tmp_res['message']}")
            else:
                results.append(tmp_res["data"])
    st.success("Done!")

    results_summary = []

    for res in results:
        results_summary.append({key: res[key] for key in consts.property_fields})

    df = pd.DataFrame(results_summary)

    st.write("Following are the results:")
    st.write(df)

    st.download_button(
        label="Download as result.csv",
        data=df.to_csv(),
        file_name="result.csv",
        mime="text/csv",
    )
