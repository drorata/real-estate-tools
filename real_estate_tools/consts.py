from typing import Any

from loguru import logger
from pydantic import BaseModel, ValidationInfo, field_validator


class ZP_Data(BaseModel):
    zpid: int
    city: str
    streetAddress: str
    state: str
    homeStatus: str
    homeType: str
    price: int
    yearBuilt: int
    lotAreaUnits: str
    lotAreaValue: float
    livingArea: int
    bedrooms: int
    bathrooms: int
    # TODO: Build a subclass to handle the price history
    priceHistory: Any
    description: str
    latitude: float
    longitude: float
    # TODO: Build a subclass to handle the list of pictures
    photos: Any

    @field_validator("lotAreaValue")
    @classmethod
    def align_lot_area_units(cls, v: float, info: ValidationInfo) -> str:
        """The lot area data is split across two fields: lotAreaValue and lotAreaUnits.
        To play safe, if the unit is not 'Square Feet', we nullify the value and log
        a warning.
        """
        if info.data["lotAreaUnits"] != "Square Feet":
            logger.warning(
                f"The value of 'lotAreaUnits' for ZPID {info.data['zpid']} is "
                f"'{info.data['lotAreaUnits']}' and not 'Square Feet'."
                "Unknown unit! Reverting to NONE"
            )
            return None
        return v
