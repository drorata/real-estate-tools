from typing import List

import requests
from loguru import logger

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
