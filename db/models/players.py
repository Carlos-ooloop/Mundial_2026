from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional

class Position(str,Enum):
    GK ="Goalkeeper"
    DF = "Defender"
    MC = "Midfielder"
    FW = "Forward"
    
class Player(BaseModel):
    id : Optional[str] = None
    age : int = Field (ge=15,le=45)
    name: str
    sur_name : str
    position : Position
    club: str
    national_team : str
    
    assits: Optional[int] = None
    goals : Optional[int] = None
    goal_contributions : Optional[int] = None
    
    saves : Optional[int] = None
    clean_sheets :Optional[int] = None
    
    tackles : Optional[int] = None
    interceptions : Optional[int] = None
    
    shots:Optional[int]= None 
    shots_on_target:Optional[int] = None
    
    @model_validator (mode="after")
    def validate_shots(self):
        if self.shots_on_target > self.shots:
            raise ValueError("SHOTS_ON_TARGET DEBE SER MENOR O IGUAL A SHOTS") 
        return self
    