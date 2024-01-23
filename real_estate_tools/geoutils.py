import time
from typing import Dict, Union

import pandas as pd
import requests
from geopy import distance
from loguru import logger

from real_estate_tools.consts import Settings

settings = Settings()


class UnsupportedGeoDecoderBackend(Exception):
    supported_backends = ["locationiq"]


def compute_distance_in_df(
    ref_lat: float,
    ref_lon: float,
    df: pd.DataFrame,
    lat_col_name: str = "lat",
    lon_col_name: str = "lon",
    new_col_name: str = "dist",
    inplace: bool = False,
):
    if not inplace:
        df = df.copy(deep=True)

    df[new_col_name] = df.apply(
        lambda x: distance.distance(
            (ref_lat, ref_lon), (x[lat_col_name], x[lon_col_name])
        ).km,
        axis=1,
    )

    return df


def _forward_search_locationiq(address: str) -> Dict[str, Union[str, float]]:
    url = settings.locationiq_forward_search_url
    data = {
        "key": settings.locationiq_api_key,
        "q": address,
        "addressdetails": 1,
        "format": "json",
    }

    # Avoid too frequent calls to the (free) API
    time.sleep(1)
    response = requests.get(url, params=data)
    if response.status_code == 200:
        response = response.json()
        if isinstance(response, list) and len(response) != 1:
            logger.warning(
                f"LocationIQ returned {len(response)} results. Expected one result"
            )
        return response[0]
    raise RuntimeError(f"response status code: {response.status_code}")


def forward_search(address: str, backend: str = "locationiq"):
    if backend not in UnsupportedGeoDecoderBackend.supported_backends:
        raise UnsupportedGeoDecoderBackend

    if backend == "locationiq":
        return _forward_search_locationiq(address)
