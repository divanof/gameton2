import os
from dotenv import load_dotenv

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pydantic import BaseModel

load_dotenv()
app = FastAPI()

PORT =  os.environ.get("PORT")

class ActionInfo(BaseModel):
    x: int
    y: int
    action: str

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    print(os.environ)
    return {"message": PORT}

@app.get("/map/")
async def get_map():
    """
    Получение карты для отрисовки
    """
    array = [
            [1, 2, 3, 3, 2, 1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 3],
            [2, 2, 2, 1, 3, 2, 2, 2, 1, 3, 3, 2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 3, 2, 1, 2, 1, 3],
            [1, 2, 3, 3, 2, 1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 3],
            [2, 2, 2, 1, 3, 2, 2, 2, 1, 3, 3, 2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 3, 2, 1, 2, 1, 3],
            [1, 2, 3, 1, 3, 1, 2, 3, 1, 3, 3, 1, 2, 3, 1, 3],
            [1, 2, 3, 3, 2, 1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 3],
            [2, 2, 2, 1, 3, 2, 2, 2, 1, 3, 3, 2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 3, 2, 1, 2, 1, 3],
            [1, 2, 3, 1, 3, 1, 2, 3, 1, 3, 3, 1, 2, 3, 1, 3],
            [1, 2, 3, 3, 2, 1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 3],
            [2, 2, 2, 1, 3, 2, 2, 2, 1, 3, 3, 2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3, 2, 1, 2, 1, 3, 3, 2, 1, 2, 1, 3],
            [1, 2, 3, 1, 3, 1, 2, 3, 1, 3, 3, 1, 2, 3, 1, 3],
            [1, 2, 3, 1, 3, 1, 2, 3, 1, 3, 3, 1, 2, 3, 1, 3],
        ];
    return {"map": array}

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
