import Optional
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # 🔑 서비스 키 경로
firebase_admin.initialize_app(cred)
db = firestore.client()

# 브랜드 추가
def add_brand(name: str, established_year:int, description: str = "", country: str = "",  ):
    brand_ref = db.collection("brands").add({
        "name": name,
        "description": description,
        "country": country,
        "established_year": established_year
    })
    return brand_ref[1].id

# 위스키 추가
def add_whisky(name: str, description: str , abv: float, genre: str, brand_id: str, cask_type:str):
    whisky_ref = db.collection("whiskies").add({
        "name": name,
        "description": description,
        "abv": abv,
        "genre": genre,
        "brand_id": brand_id,
        "cask_type":cask_type
    })
    return whisky_ref[1].id

# 사용자 평가 추가
def add_tasting_note(user_id: str, whisky_id: str, note: str, flavor_wheel=None, flavor_label=None):
    db.collection("tasting_notes").add({
        "user_id": user_id,
        "whisky_id": whisky_id,
        "note": note,
        "flavor_wheel": flavor_wheel or [],
        "flavor_label": flavor_label or []
    })

# 수집 장소 추가
def add_location(name: str):
    loc_ref = db.collection("locations").add({
        "name": name
    })
    return loc_ref[1].id

# 가격 데이터 추가
def add_price(whisky_id: str, year: int, month: int, location_id: str, price: int):
    db.collection("prices").add({
        "whisky_id": whisky_id,
        "year": year,
        "month": month,
        "location_id": location_id,
        "price": price
    })

# 예시 사용
if __name__ == "__main__":
    # 브랜드 추가
    brand_id = add_brand("산토리")

    # 위스키 추가
    whisky_id = add_whisky("야마자키 12년", abv=43.0, genre="싱글몰트", brand_id=brand_id)

    # 장소 추가
    location_id = add_location("코스트코")

    # 가격 추가
    add_price(whisky_id, 2025, 7, location_id, 180000)

    # 평가 추가
    # add_tasting_note(user_id="user_123", whisky_id=whisky_id, note="부드럽고 과일향이 인상적임")

    print("샘플 데이터가 업로드되었습니다.")
