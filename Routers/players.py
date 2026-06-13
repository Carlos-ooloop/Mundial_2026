from fastapi import FastAPI, APIRouter,status,HTTPException,Depends
from db.models.players import Player, Position
from db.client import db_client
from Routers.autentificacion import auth_user,admin_required
from db.schemas.player import player_schema, players_schemas
from bson import ObjectId

exception_not_found = HTTPException(status_code=404, detail="NO SE ENCONTRO EL JUGADOR")
router = APIRouter(prefix="/players", tags=["players"],dependencies=[Depends(auth_user)])


def buscar_player(field:str, key):
    
      player = db_client.local.players.find_one({field:key})
      if player is None:
         raise exception_not_found
      return Player(**player_schema(player)) 
   
          

@router.post("/", dependencies = [Depends(admin_required)])
async def add_player(player:Player):
   
    player_dict = dict(player)
    if db_client.local.players.find_one({"sur_name":player_dict["sur_name"]}):
        return {"EL JUGADOR YA EXISTE"}
    
    del player_dict["id"]
        
    id = db_client.local.players.insert_one(player_dict).inserted_id
    new_player = player_schema(db_client.local.players.find_one({"_id": ObjectId(id)}))
    return new_player
 
@router.get("/")
async def get_query(position:str|None=None, selection:str|None=None, club:str|None=None):
   query = dict() 
   if position:
      query["position"] = position
   if selection:
      query["national_team"] = selection
   if club:
      query["club"] = club
   return players_schemas(db_client.local.players.find(query))

      
@router.get("/name")
async def get_player(player_name:str):
   return players_schemas(db_client.local.players.find({"name":player_name}))
@router.get("/position")
async def get_player_by_position(position:Position):
   return  players_schemas(db_client.local.players.find({"position":position}))
@router.get("/national_team")
async def get_player_by_national_team(national_team:str):
   return  players_schemas(db_client.local.players.find({"national_team":national_team}))
@router.get("/club")
async def get_player_by_club(club:str):
   return  players_schemas(db_client.local.players.find({"club":club}))
@router.get("/")
async def get_player():
   return players_schemas(db_client.local.players.find())
@router.get("/")
async def get_player(page:int = 1, limit:int=10):
   skip = (page - 1)*limit
   return players_schemas(db_client.local.players.find().skip(skip).limit(limit))



@router.put("/", dependencies=[Depends(admin_required)])
async def act_player(player:Player):
    player_dict = dict(player)
    del player_dict["id"]
    try:
      db_client.local.players.find_one_and_replace({"_id": ObjectId(player.id)},player_dict)
    except:
      raise exception_not_found
    return player_dict
 
 
@router.delete("/",dependencies=[Depends(admin_required)])
async def  delete_player(player:Player):
   try:
     db_client.local.players.find_one_and_delete({"_id":ObjectId(player.id)})
     return "JUGADOR ELIMINADO"
   except:
     return exception_not_found  
  
   
@router.get("/topscorers")
async def top_scorers():
   return players_schemas(db_client.local.players.find().sort("goals", -1)) 
@router.get("/topsassits")
async def top_assits():
   return players_schemas(db_client.local.players.find().sort("assits", -1)) 

    
  
  
 
 
 
    
    
