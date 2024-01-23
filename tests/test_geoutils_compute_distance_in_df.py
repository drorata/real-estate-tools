import pandas as pd
import pytest

from real_estate_tools.geoutils import compute_distance_in_df


@pytest.fixture
def ref_lat_lon():
    ref_lat = 52.52464141812648
    ref_lon = 13.367240539754226
    return (ref_lat, ref_lon)


@pytest.fixture
def input_df(ref_lat_lon):
    ref_lat, ref_lon = ref_lat_lon
    return pd.DataFrame({
        "lat": [ref_lat, 52.518377700734035, 52.52021871916864],
        "lon": [ref_lon, 13.3756894979551, 13.369220010065687],
    })


@pytest.fixture
def expected_distances():
    return [0, 0.9026147253527895, 0.5101563827091723]


def test_basic(ref_lat_lon, input_df, expected_distances):
    ref_lat, ref_lon = ref_lat_lon

    df = input_df

    result = compute_distance_in_df(ref_lat=ref_lat, ref_lon=ref_lon, df=df)

    expected_res = df.copy(deep=True)
    expected_res["dist"] = expected_distances

    assert "dist" not in df.columns
    pd.testing.assert_frame_equal(result, expected_res)


def test_basic_inplace(ref_lat_lon, input_df, expected_distances):
    ref_lat, ref_lon = ref_lat_lon
    df = input_df

    result = compute_distance_in_df(
        ref_lat=ref_lat, ref_lon=ref_lon, df=df, inplace=True
    )

    expected_res = df.copy(deep=True)
    expected_res["dist"] = expected_distances

    assert "dist" in df.columns
    pd.testing.assert_frame_equal(result, expected_res)
    pd.testing.assert_frame_equal(result, df)
