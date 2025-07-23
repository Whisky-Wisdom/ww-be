from typing import List, Optional
from app.features.whisky.model.whisky_schema import Location

locations: List[Location] = []

def create_location(location: Location) -> Location:
    locations.append(location)
    return location

def get_location(name: str) -> Optional[Location]:
    for l in locations:
        if l.name == name:
            return l
    return None

def update_location(name: str, location_update: Location) -> Optional[Location]:
    for idx, l in enumerate(locations):
        if l.name == name:
            locations[idx] = location_update
            return location_update
    return None

def delete_location(name: str) -> bool:
    global locations
    for idx, l in enumerate(locations):
        if l.name == name:
            del locations[idx]
            return True
    return False
