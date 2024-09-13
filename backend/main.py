from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

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
    return {"message": "Hello World!"}

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
    Отправка события на сервер
    """
    x = action.x
    y = action.y
    action_type = action.action

    return {"x": x, "y": y, "action": action_type}
