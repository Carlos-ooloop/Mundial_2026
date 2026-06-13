from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from datetime import datetime, timedelta
from pydantic import BaseModel
from db.client import db_client
from db.schemas.user import user_schema, users_schemas
from db.models.user   import Users, UserDB
from datetime import datetime, timedelta
from Routers.autentificacion import buscar_usuario
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
router = APIRouter(prefix="/users",tags=["users"])

def exception_not_found():
    raise HTTPException(status_code=404,detail="Usuario no encontrado")


@router.post("/register")
async def add_user(user:UserDB):
 
     user_dict = dict(user)
     if db_client.local.users.find_one({"email":user_dict["email"]}):
         return "EL USUARIO YA EXISTE"
     del user_dict["id"]
     
     hashed_password = pwd_context.hash(user.password)
     user_dict["password"]= hashed_password
     id = db_client.local.users.insert_one(user_dict).inserted_id
    
     new_user = user_schema(db_client.local.users.find_one({"_id":ObjectId(id)}))
     return Users(**new_user)
    
@router.get("/")
async def get_user():
     return users_schemas(db_client.local.users.find())  
 
@router.put("/")
async def act_user(user:Users):
     user_dict = dict(user)
     del user_dict["id"]
     try:
         db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)} ,user_dict)
     except:
         return exception_not_found    
     return user_dict
@router.delete("/")
async def delete_user(user:Users):
    try:
        db_client.local.users.find_one_and_delete({"_id":ObjectId(user.id)})
        return "USUARIO ELIMINADO"
    except:
        return exception_not_found
        
 
 
 
 