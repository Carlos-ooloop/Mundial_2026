from Routers import autentificacion, players, users,selection
from fastapi import FastAPI, APIRouter,status
from pydantic import BaseModel

app = FastAPI()

app.include_router(autentificacion.router)
app.include_router(users.router)
app.include_router(players.router)
app.include_router(selection.router)



