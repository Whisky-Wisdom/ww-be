from typing import List, Optional
from app.features.whisky.model.whisky_schema import Price

prices: List[Price] = []

def create_price(price: Price) -> Price:
    prices.append(price)
    return price

def get_price(whisky_id: str, year: int, month: int, location_id: str) -> Optional[Price]:
    for p in prices:
        if p.whisky_id == whisky_id and p.year == year and p.month == month and p.location_id == location_id:
            return p
    return None

def update_price(whisky_id: str, year: int, month: int, location_id: str, price_update: Price) -> Optional[Price]:
    for idx, p in enumerate(prices):
        if p.whisky_id == whisky_id and p.year == year and p.month == month and p.location_id == location_id:
            prices[idx] = price_update
            return price_update
    return None

def delete_price(whisky_id: str, year: int, month: int, location_id: str) -> bool:
    global prices
    for idx, p in enumerate(prices):
        if p.whisky_id == whisky_id and p.year == year and p.month == month and p.location_id == location_id:
            del prices[idx]
            return True
    return False
