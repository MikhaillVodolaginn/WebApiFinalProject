from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Country
class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    name: Optional[str] = None


class Country(CountryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# City
class CityBase(BaseModel):
    name: str
    country_id: int


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None
    country_id: Optional[str] = None


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# Street
class StreetBase(BaseModel):
    name: str
    city_id: int


class StreetCreate(StreetBase):
    pass


class StreetUpdate(StreetBase):
    name: Optional[str] = None
    city_id: Optional[int] = None


class Street(StreetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
