import pandas as pd
import streamlit as st
from loguru import logger

from real_estate_tools.utils import clean_zpid, fetch_properties

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
        results = fetch_properties(api_key=api_key, zpids=zpids)
    st.success("Done!")

    df = pd.DataFrame([x.model_dump() for x in results])

    st.write("Following are the results:")
    st.write(df)

    st.download_button(
        label="Download as result.csv",
        data=df.to_csv(),
        file_name="result.csv",
        mime="text/csv",
    )
