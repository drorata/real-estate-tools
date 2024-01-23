import json
from datetime import date
from typing import Any, Union

from loguru import logger
from pydantic import BaseModel, Field, HttpUrl, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="RET_"
    )
    scrapeak_api_key: str
    scrapeak_zillow_url: str
    locationiq_api_key: str
    locationiq_forward_search_url: str
    google_credentials_type: str
    google_credentials_project_id: str
    google_credentials_private_key_id: str
    google_credentials_private_key: str
    google_credentials_client_email: str
    google_credentials_client_id: str
    google_credentials_auth_uri: str
    google_credentials_token_uri: str
    google_credentials_auth_provider_x509_cert_url: str
    google_credentials_client_x509_cert_url: str
    google_credentials_universe_domain: str

    def get_google_credentials_as_dict(self):
        return {  # pragma: no cover
            "auth_provider_x509_cert_url": (
                self.google_credentials_auth_provider_x509_cert_url
            ),
            "auth_uri": self.google_credentials_auth_uri,
            "client_email": self.google_credentials_client_email,
            "client_id": self.google_credentials_client_id,
            "client_x509_cert_url": self.google_credentials_client_x509_cert_url,
            "private_key": self.google_credentials_private_key.replace("\\n", "\n"),
            "private_key_id": self.google_credentials_private_key_id,
            "project_id": self.google_credentials_project_id,
            "token_uri": self.google_credentials_token_uri,
            "type": self.google_credentials_type,
            "universe_domain": self.google_credentials_universe_domain,
        }

    def get_google_credentials_as_json(self):
        return json.dumps(self.get_google_credentials_as_dict())  # pragma: no cover


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


class PropertyDetails(BaseModel):
    address: str
    full_address: str
    county: str | None = None
    lat: float
    lon: float
    link: HttpUrl | None = None
    thumbnail_link: HttpUrl | None = None
    parcel_id: str | None = None
    lot_area: int
    living_area: int
    baths: float
    rooms: float
    garages: int
    built_year: int
    listed_date: date
    listed_price: int
    sold_date: date | None = None
    sold_price: int | None = None
    # TODO: Add validations to fields


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
