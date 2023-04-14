from typing import Union, List
from enum import Enum

from fastapi import FastAPI, Query, Path, Body, Cookie
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


@app.get('/')
async def root():
    return {'hello': '你好'}


# 你需要确保路径 /users/me 声明在路径 /users/{user_id}之前：
@app.get('/users/me')
async def read_user_me():
    return {'user_id': 'the current user'}


@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {'user_id': user_id}


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {'model_name': model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# 路径转换器
@app.get('/files/{file_path:path}')
async def read_file(file_path: str):
    return {'file_path': file_path}


'''
查询参数

当你为非路径参数声明了默认值时（目前而言，我们所知道的仅有查询参数），则该参数不是必需的。

如果你不想添加一个特定的值，而只是想使该参数成为可选的，则将默认值设置为 None。

但当你想让一个查询参数成为必需的，不声明任何默认值就可以：
'''
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# cookie
@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10, ads_id: Union[str, None] = Cookie(default=None)):
    return {'lists': fake_items_db[skip: skip + limit], 'cookie_id': ads_id}


@app.get('/users/{user_id}/items/{item_id}')
def read_user_item(user_id: int,
                   item_id: int = Path(title='The ID of the item to get', description='啦啦啦啦', gt=0, le=1000),
                   q: Union[str, None] = Query(default=None, min_length=3,
                                               max_length=50, alias='item-query',
                                               title='title',
                                               description='description'
                                               ),
                   short: bool = False):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})

    return item


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title='The description of the item', max_length=300
    )
    price: float = Field(ge=0, description='The price must be greater than zero')
    tax: Union[float, None] = None,
    tags: List[str] = []
    images: Union[List[Image], None] = None


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


@app.post('/offers/')
async def create_offer(offer: Offer):
    return offer


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(
        item_id: int = Path(title='The ID of the item to get', ge=0, le=1000),
        q: Union[str, None] = None,
        item: Union[Item, None] = None,
        importance: int = Body()
):
    results = {'item_id': item_id, 'importance': importance}
    if q:
        results.update({'q': q})
    if item:
        results.update({'item': item})
    return results
