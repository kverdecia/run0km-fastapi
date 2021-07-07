from typing import List
from urllib.parse import urljoin
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel

from localsettings import DATABASE_URI, MEDIA_URL


app = FastAPI(title="Run0Km API")
database = Database(DATABASE_URI, min_size=5, max_size=20)


class Item(BaseModel):
    id: int
    name: str
    code: str
    image: str

    @classmethod
    def from_row(cls, row):
        result = cls(**row)
        result.image = urljoin(MEDIA_URL, result.image)
        return result


class Brand(Item):
    pass


class Model(Item):
    pass


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/brands')
async def brand_list() -> List[Brand]:
    query = 'select id, name, code, logo as image from brands_carbrand where enabled = true'
    brands = [Brand.from_row(row) for row in await database.fetch_all(query)]
    return brands


@app.get('/brands/{brand_id}')
async def brand_item(brand_id: int) -> Brand:
    query = 'select id, name, code, logo as image from brands_carbrand where id = :brand_id and enabled = true'
    params = {'brand_id': brand_id}
    row = await database.fetch_one(query, params)
    if row is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail='brand not found')
    return Brand.from_row(row)


@app.get('/brands/{brand_id}/models')
async def brand_models(brand_id: int) -> List[Model]:
    query = '''
    select m.id, m.code, m.name, m.main_photo as image
    from brands_carbrand as b
        left join brands_carmodel as m on b.id = m.brand_id
    where brand_id = :brand_id and b.enabled = true and m.enabled = true'''
    params = {'brand_id': brand_id}
    models = [Model.from_row(row) for row in await database.fetch_all(query, params)]
    return models


@app.get('/models')
async def model_list():
    query = '''
    select m.id, m.code, m.name, m.main_photo as image
    from brands_carbrand as b
        left join brands_carmodel as m on b.id = m.brand_id
    where b.enabled = true and m.enabled = true'''
    models = [Model.from_row(row) for row in await database.fetch_all(query)]
    return models


@app.get('/models/{model_id}')
async def model_item(model_id: int) -> Model:
    query = '''
    select m.id, m.code, m.name, m.main_photo as image
    from brands_carbrand as b
        left join brands_carmodel as m on b.id = m.brand_id
    where m.id = :model_id and b.enabled = true and m.enabled = true'''
    params = {'model_id': model_id}
    row = await database.fetch_one(query, params)
    if row is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="model not found")
    return Model.from_row(row)
