import os
from dotenv import load_dotenv
from time import sleep
import json

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pydantic import BaseModel

from game_cycle import main_cycle

load_dotenv()
app = FastAPI()

PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")


class ActionInfo(BaseModel):
    x: int
    y: int
    action: str


origins = ["*"]


def json_read(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def run_game_cycle():
    print("main game cycle started")
    main_cycle()


@app.get("/")
async def main(background_tasks: BackgroundTasks):
    print(os.environ)
    # background_tasks.add_task(run_game_cycle)
    return {"message": PORT}


@app.get("/map/")
async def get_map():
    """
    Получение карты для отрисовки
    """
    units = json_read("logs/units.json")
    world = json_read("logs/world.json")

    return {"units": units, "world": world}


@app.post("/action/")
async def handle_action(action: ActionInfo):
    """
    Получение события с управляющей панели
    """
    x = action.x
    y = action.y
    action_type = action.action

    return {"x": x, "y": y, "action": action_type}


@app.post("/w_key_action/")
async def handle_w_key_action():
    """
    Получение события с управляющей панели при нажатии клавиши W
    """
    return {"key": "W"}


@app.post("/s_key_action/")
async def handle_s_key_action():
    """
    Получение события с управляющей панели при нажатии клавиши S
    """
    return {"key": "S"}


@app.post("/a_key_action/")
async def handle_a_key_action():
    """
    Получение события с управляющей панели при нажатии клавиши A
    """
    return {"key": "A"}


@app.post("/d_key_action/")
async def handle_d_key_action():
    """
    Получение события с управляющей панели при нажатии клавиши D
    """
    return {"key": "D"}


@app.post("/space_key_action/")
async def handle_space_key_action():
    """
    Получение события с управляющей панели при нажатии клавиши пробела
    """
    return {"key": " "}
