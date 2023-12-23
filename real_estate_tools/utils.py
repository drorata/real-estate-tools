from typing import List

import pandas as pd
import requests
from loguru import logger
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from real_estate_tools.consts import ZP_Data


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
