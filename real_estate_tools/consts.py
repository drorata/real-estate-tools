from typing import Any, Union

from loguru import logger
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class SellPurchaseFactors(BaseModel):
    broker_commission: Union[int, float] = Field(gt=0, lt=1)
    fixed_broker_fee: Union[int, float]
    closing_costs: Union[int, float] = Field(ge=0, lt=1)
    transfer_tax: Union[int, float] = Field(ge=0, lt=1)
    fixed_notary: Union[int, float]
    deed_recording_fee: Union[int, float]
    legal_fee: Union[int, float]

    def get_cost(self, price: float) -> float:
        return (
            price * self.broker_commission
            + self.fixed_broker_fee
            + price * self.closing_costs
            + price * self.transfer_tax
            + self.fixed_notary
            + self.deed_recording_fee
            + self.legal_fee
        )


class ZP_Data(BaseModel):
    zpid: int
    parcelId: str
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
