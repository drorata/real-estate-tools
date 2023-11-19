import pandas as pd
import streamlit as st
from loguru import logger

from real_estate_tools.consts import ZP_Data
from real_estate_tools.utils import clean_zpid, get_property_detail

logger.info("ARV estimator started")


api_key = st.text_input("Provide API key", type="password")

zpids = st.text_input("Provide a ZPIDs (separated with commas)")
zpids = zpids.split(",")
zpids = [clean_zpid(zpid) for zpid in zpids]
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
                results.append(ZP_Data(**tmp_res["data"]))
    st.success("Done!")

    df = pd.DataFrame([x.dict() for x in results])

    st.write("Following are the results:")
    st.write(df)

    st.download_button(
        label="Download as result.csv",
        data=df.to_csv(),
        file_name="result.csv",
        mime="text/csv",
    )
