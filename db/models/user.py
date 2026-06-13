from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
   username: str
   id : Optional[str] = None
   email : str
   role : str = "user"
class UserDB(Users):
   password :str  