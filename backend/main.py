from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

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
    array = [
            [1, 2, 3, 3, 2],
            [2, 2, 2, 1, 3],
            [2, 1, 2, 1, 3],
            [1, 2, 3, 1, 3]
        ];
    return {"map": array}
