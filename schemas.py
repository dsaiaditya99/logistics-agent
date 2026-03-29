from pydantic import BaseModel
from typing import List

class LocationRequest(BaseModel):
    query: str
    locations: List[List[float]] = []