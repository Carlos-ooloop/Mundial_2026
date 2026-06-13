from fastapi import FastAPI, APIRouter,status,HTTPException,Depends
from db.models.players import Player, Position
from db.models.selection import Selection
from db.client import db_client
from Routers.autentificacion import auth_user
from db.schemas.player import player_schema, players_schemas
from db.schemas.selection import selection_schema, selection_schemas
from bson import ObjectId


exception_not_found = HTTPException(status_code=404, detail="NO SE ENCONTRO LA SELECCION")
router = APIRouter(prefix="/selection", tags=["selection"],dependencies=[Depends(auth_user)])


def buscar_seleccion(field:str,key):
      selection = db_client.local.selection.find_one({field:key})
      if selection is None:
         raise exception_not_found
      return Selection(**selection_schema(selection)) 
   
@router.post("/")
async def add_selection(selection:Selection):
    selection_dict = dict(selection)
    del selection_dict["id"]
    id = db_client.local.selection.insert_one(selection_dict).inserted_id
    new_selection = selection_schema(db_client.local.selection.find_one({ "_id": ObjectId(id) }))
    return new_selection

@router.get("/")
async def get_selection():
    return selection_schemas(db_client.local.selection.find())

@router.get("/{selection_id}/players")
async def get_selection_players(selection_id:str):
    selection_dict = dict(buscar_seleccion("_id",ObjectId(selection_id)))
  
    return list(players_schemas(db_client.local.players.find({"national_team":selection_dict["name"]})))
    
    