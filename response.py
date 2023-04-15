from typing import Any, List, Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float = 10.5
    tax: Union[float, None] = None
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.post('/items/', response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get('/items/', response_model=List[Item])
async def read_items() -> Any:
    return [
        {'name': 'Portal Gun', 'price': 42.0},
        {'name': 'Jessey', 'price': 62.0},
    ]


@app.get('/items/{item_id}', response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get('/items/{item_id}/name', response_model=Item, response_model_include={'name', 'description', 'price'})
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post('/users/', response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


















