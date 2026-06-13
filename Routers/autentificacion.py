from jose import jwt, JWTError
from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from db.client import db_client
from db.schemas.user import user_schema
from db.models.user   import Users, UserDB
from db.models.refresh_token import RefreshTokenRequest
from datetime import datetime, timedelta



ALGORITHM = "HS256"
SECRET = "c58c87349fe778beecdd92f9cd3467d1cf0fb829b747dac15787cc44d61e3298"
TOKEN_DURATION_TIME = 10
router = APIRouter()
encriptacion = CryptContext(schemes="bcrypt")
oauth = OAuth2PasswordBearer(tokenUrl="/login")


def crear_refresh_token(data:dict):
    cript = data.copy()
    expire = datetime.utcnow()+timedelta(days = 7)
    cript.update({"exp":expire})
    return jwt.encode(cript,SECRET,algorithm="HS256")


def exception_not_found():
    raise HTTPException(status_code=404,detail="Usuario no encontrado")


def buscar_usuario(field: str, key):
    user = db_client.local.users.find_one({field: key})
  
    if user is None:
        exception_not_found()
        
    return UserDB(**user_schema(user))



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = buscar_usuario("username",form.username)
   
    if not encriptacion.verify(form.password, user.password):
        raise HTTPException(status_code=402, detail="CONTRASEÑA INCORRECTA")
    
    expiracion = datetime.utcnow() + timedelta(minutes=TOKEN_DURATION_TIME)
    acces_token = {"sub": user.username, "exp":expiracion}
    refresh_token = crear_refresh_token({"sub":user.username})
    
    return {"ACCESS_TOKEN": jwt.encode(acces_token,SECRET,algorithm=ALGORITHM),"REFRESH_TOKEN":refresh_token,"TOKEN_TYPE":"BEARER"}




@router.post("/login/auth")
async def auth_user(token:str = Depends(oauth)):
    if not token:
        raise HTTPException(status_code=401, detail={"DEBE AUTENTICARSE PARA ACCEDER A ESTE RECURSO"})
    try:
     username = jwt.decode(token,SECRET, algorithms=ALGORITHM).get("sub")
     if username == None:
        raise HTTPException(status_code=402,detail="CREDENCIALES NO VALIDAS")
    except JWTError:
        raise HTTPException(status_code=402,detail="CREDENCIALES NO VALIDAS")
    
    return buscar_usuario("username",username)



@router.get("/user/me")
async def me(user:Users = Depends(auth_user)):
    return user



async def admin_required(current_user:Users = Depends(auth_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="NO TIENE PERMISOS DE ADMINISTRADOR")
    return current_user    



@router.post("/refresh")
async def refresh(token:RefreshTokenRequest):
    try:
        refresh_token = jwt.decode(token,SECRET,algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401,detail="REFRESH TOKEN INVALIDO")
    username = refresh_token.get("sub")
    user = buscar_usuario("username", username)
    expiracion = datetime.utcnow()+timedelta(minutes=TOKEN_DURATION_TIME)
    new_access_token = { "sub": user.username , "exp":expiracion}
    
    return {"ACCESS_TOKEN":jwt.encode(new_access_token,SECRET,algorithm=ALGORITHM),"TOKEN_TYPE":"BEARER"}    
        

  
    