from pydantic import BaseModel, parse_obj_as
from typing import Dict, List

class DataDict(BaseModel):
    prompt: str
    temperature: float
    max_new_tokens: int

class DataBody(BaseModel):
    model: str
    messages: List[DataDict]
