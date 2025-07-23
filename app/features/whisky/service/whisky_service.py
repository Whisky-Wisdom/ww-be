from typing import List, Optional
from app.features.whisky.model.whisky_schema import Brand, Whisky, Location, Price

whiskies: List[Whisky] = []

def create_whisky(whisky: Whisky) -> Whisky:
    whiskies.append(whisky)
    return whisky

def get_whisky(name_kr: str) -> Optional[Whisky]:
    for w in whiskies:
        if w.name_kr == name_kr:
            return w
    return None

def update_whisky(name_kr: str, whisky_update: Whisky) -> Optional[Whisky]:
    for idx, w in enumerate(whiskies):
        if w.name_kr == name_kr:
            whiskies[idx] = whisky_update
            return whisky_update
    return None

def delete_whisky(name_kr: str) -> bool:
    global whiskies
    for idx, w in enumerate(whiskies):
        if w.name_kr == name_kr:
            del whiskies[idx]
            return True
    return False

