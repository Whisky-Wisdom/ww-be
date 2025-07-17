from fastapi import APIRouter, Request

from app.db.firebase import add_brand, add_whisky, add_location, add_price

router = APIRouter(prefix="/whisky")


@router.get("/a")
async def process_collect_data(request: Request):



    brand_id = add_brand(
        name_kr="산토리",
        name_en="Suntory",
        description_kr="일본의 대표적인 주류 브랜드",
        description_en="A leading Japanese alcoholic beverage company",
        country="Japan",
        keywords=["일본", "산토리"]
    )

    # 위스키 추가
    whisky_id = add_whisky(
        name_kr="야마자키 12년",
        name_en="Yamazaki 12 Years Old",
        description_kr="부드럽고 깊은 맛의 싱글몰트",
        description_en="A smooth and rich single malt whisky",
        abv=43.0,
        genre="싱글몰트",
        brand_id=brand_id,
        cask_type="버번",
        keywords=["야마자키", "12년", "싱글몰트", "Yamazaki"]
    )

    # 장소 추가
    location_id = add_location("코스트코")

    # 가격 추가
    add_price(whisky_id, 2025, 7, location_id, 180000)

    # 평가 추가
    # add_tasting_note(user_id="user_123", whisky_id=whisky_id, note="부드럽고 과일향이 인상적임")

    print("샘플 데이터가 업로드되었습니다.")


    return {"asdasd":"aasdasdasdasdasd"}
