from typing import List, Optional
from app.features.whisky.model.whisky_schema import Brand

# 임시 저장소 (실제 DB로 대체 필요)
brands: List[Brand] = []

def create_brand(brand: Brand) -> Brand:
    brands.append(brand)
    return brand

def get_brand(name_kr: str) -> Optional[Brand]:
    for b in brands:
        if b.name_kr == name_kr:
            return b
    return None

def update_brand(name_kr: str, brand_update: Brand) -> Optional[Brand]:
    for idx, b in enumerate(brands):
        if b.name_kr == name_kr:
            brands[idx] = brand_update
            return brand_update
    return None

def delete_brand(name_kr: str) -> bool:
    global brands
    for idx, b in enumerate(brands):
        if b.name_kr == name_kr:
            del brands[idx]
            return True
    return False
