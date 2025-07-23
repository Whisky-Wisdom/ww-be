from fastapi import APIRouter, HTTPException, Request
from app.features.whisky.model.whisky_schema import Brand, Whisky, Location, Price
from app.features.whisky.service.brand_service import create_brand, get_brand, update_brand, delete_brand
from app.features.whisky.service.location_service import create_location, get_location, delete_location, update_location
from app.features.whisky.service.price_service import delete_price, update_price, get_price, create_price
from app.features.whisky.service.whisky_service import create_whisky, get_whisky, update_whisky, delete_whisky
from app.features.whisky.collector.router import router as collector_router

router = APIRouter(prefix="/whisky")


router.include_router(collector_router)


# Brand CRUD
@router.post("/brand", response_model=Brand)
def add_brand(brand: Brand):
    return create_brand(brand)

@router.get("/brand/{name_kr}", response_model=Brand)
def read_brand(name_kr: str):
    brand = get_brand(name_kr)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put("/brand/{name_kr}", response_model=Brand)
def update_brand_route(name_kr: str, brand: Brand):
    updated = update_brand(name_kr, brand)
    if not updated:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated

@router.delete("/brand/{name_kr}")
def delete_brand_route(name_kr: str):
    if not delete_brand(name_kr):
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"ok": True}

# Whisky CRUD
@router.post("/whisky", response_model=Whisky)
def add_whisky(whisky: Whisky):
    return create_whisky(whisky)

@router.get("/whisky/{name_kr}", response_model=Whisky)
def read_whisky(name_kr: str):
    whisky = get_whisky(name_kr)
    if not whisky:
        raise HTTPException(status_code=404, detail="Whisky not found")
    return whisky

@router.put("/whisky/{name_kr}", response_model=Whisky)
def update_whisky_route(name_kr: str, whisky: Whisky):
    updated = update_whisky(name_kr, whisky)
    if not updated:
        raise HTTPException(status_code=404, detail="Whisky not found")
    return updated

@router.delete("/whisky/{name_kr}")
def delete_whisky_route(name_kr: str):
    if not delete_whisky(name_kr):
        raise HTTPException(status_code=404, detail="Whisky not found")
    return {"ok": True}

# Location CRUD
@router.post("/location", response_model=Location)
def add_location(location: Location):
    return create_location(location)

@router.get("/location/{name}", response_model=Location)
def read_location(name: str):
    location = get_location(name)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.put("/location/{name}", response_model=Location)
def update_location_route(name: str, location: Location):
    updated = update_location(name, location)
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated

@router.delete("/location/{name}")
def delete_location_route(name: str):
    if not delete_location(name):
        raise HTTPException(status_code=404, detail="Location not found")
    return {"ok": True}

# Price CRUD
@router.post("/price", response_model=Price)
def add_price(price: Price):
    return create_price(price)

@router.get("/price/{whisky_id}/{year}/{month}/{location_id}", response_model=Price)
def read_price(whisky_id: str, year: int, month: int, location_id: str):
    price = get_price(whisky_id, year, month, location_id)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price

@router.put("/price/{whisky_id}/{year}/{month}/{location_id}", response_model=Price)
def update_price_route(whisky_id: str, year: int, month: int, location_id: str, price: Price):
    updated = update_price(whisky_id, year, month, location_id, price)
    if not updated:
        raise HTTPException(status_code=404, detail="Price not found")
    return updated

@router.delete("/price/{whisky_id}/{year}/{month}/{location_id}")
def delete_price_route(whisky_id: str, year: int, month: int, location_id: str):
    if not delete_price(whisky_id, year, month, location_id):
        raise HTTPException(status_code=404, detail="Price not found")
    return {"ok": True}


