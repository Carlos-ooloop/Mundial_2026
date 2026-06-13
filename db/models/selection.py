from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Selection(BaseModel):
    id : Optional[str] = None
    name : str
    coach : str
    ranking_fifa : int