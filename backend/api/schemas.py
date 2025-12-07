from pydantic import BaseModel, ConfigDict
from typing import List

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]