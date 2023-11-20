import requests


def clean_zpid(zpid: str) -> str:
    return zpid.split("_")[0]


def get_property_detail(
    api_key: str, zpid: str
) -> requests.Response:  # pragma: no cover
    url = "https://app.scrapeak.com/v1/scrapers/zillow/property"
    querystring = {"api_key": api_key, "zpid": zpid}
    return requests.request("GET", url, params=querystring)
