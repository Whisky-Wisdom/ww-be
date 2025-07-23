from app.features.whisky.service.brand_service import create_brand, get_brand
from app.features.whisky.service.location_service import create_location, get_location
from app.features.whisky.service.price_service import create_price, get_price
from app.features.whisky.model.whisky_schema import Brand, Whisky, Location, Price
from app.features.whisky.service.whisky_service import get_whisky, create_whisky


def save_whisky_info_to_firestore(whisky_infos):

    for info in whisky_infos:
        # 1. 브랜드 저장 또는 조회
        brand_name = info.get("brand")
        brand_obj = get_brand(brand_name)
        if not brand_obj:
            brand_obj = create_brand(Brand(name_kr=brand_name))

        # 2. 위스키 저장 또는 조회
        whisky_name = info.get("name_age")
        volume = info.get("volume_ml")
        whisky_obj = get_whisky(whisky_name)
        if not whisky_obj:
            whisky_obj = create_whisky(Whisky(name_kr=whisky_name, volume=volume, brand_id=brand_name))

        # 3. 장소 저장 또는 조회
        location_name = info.get("location")
        location_obj = get_location(location_name)
        if not location_obj:
            location_obj = create_location(Location(name=location_name))

        # 4. 가격 정보 저장 (Price)
        price = info.get("price_krw")
        date = info.get("date")
        # 년/월 추출
        if date:
            year, month = int(date[:4]), int(date[5:7])
        else:
            year, month = None, None

        if whisky_obj and location_obj and price is not None and year and month:
            create_price(Price(
                whisky_id=whisky_obj.name_kr,
                year=year,
                month=month,
                location_id=location_name,
                price=price
            ))