# state.py
from typing import List, Optional
from pydantic import BaseModel

class GraphState(BaseModel):
    url: str
    image_urls: List[str] = []
    error: Optional[str] = None
