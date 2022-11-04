from datetime import datetime
from typing import List

from pydantic import BaseModel


class DocumentScheme(BaseModel):
    rubrics: List[str]
    text: str
    created_date: datetime
