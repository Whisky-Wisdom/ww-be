from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime



class Brand(BaseModel):
    name_kr: str
    name_en: Optional[str] = None
    description_kr: Optional[str] = None
    description_en: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = None


class Whisky(BaseModel):
    name_kr:  str
    volume: Optional[int] = Field(default=None, ge=0) # (ml)
    name_en: Optional[str] = None
    description_kr: Optional[str] = None
    description_en: Optional[str] = None
    abv: Optional[float] = Field(default=None, ge=0, le=100) #도수
    genre: Optional[str] = None #싱글몰트 블랜디드 버번 쉐리
    brand_id: Optional[str] = None
    tags: Optional[List[str]] = None
    is_limited: Optional[bool] = False
    is_discontinued: Optional[bool] = False


class Location(BaseModel):
    name: Optional[str] = None


class Price(BaseModel):
    whisky_id:  str
    year: int
    month: int
    location_id: str
    price: int
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)