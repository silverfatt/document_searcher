from pydantic import BaseModel
from typing import List


class DocumentScheme(BaseModel):
    rubrics: List[str]
    text: str
