from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Укажите разрешенные источники
origins = [
    "*"
    # Добавьте другие источники по необходимости
]

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,  # Разрешить использование учетных данных
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.get("/")
async def main():
    return {"message": "Hello World!"}

@app.post("/items/")
async def create_item(item: Item):
    return item
