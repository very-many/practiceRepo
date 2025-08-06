import random
from enum import Enum
from typing import Annotated

from pydantic import BaseModel
from pydantic import AfterValidator
from fastapi import FastAPI, Query, Path

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


class Champion(str, Enum):
    samira = "samira"
    darius = "darius"
    leblanc = "leblanc"


@app.get("/")
def read_root():
    return {"Hello": "World"}


# --------------------------------------------------------------------------------------------------


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": f'Item {item_id} the great item from user{user_id} with <<{q if q else "no query"}>> as q. Wahtever q means.'
            }
        )
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# --------------------------------------------------------------------------------------------------


# Query parameters are automatically converted to defined type
# Query parameters are required here, no default value
@app.get("/add")
def update_item(a: int, b: int):
    return {"Sum": a + b}


# --------------------------------------------------------------------------------------------------


# Evaluated in order! `/users/me` before `/users/{user_id}`
@app.get("/users/me")
def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}


# --------------------------------------------------------------------------------------------------


@app.get("/wiki/{champion}")
def get_wiki_champion(champion: Champion):

    # In Python, only functions, classes, and modules introduce a new scope.
    # Control flow blocks like match, if, for, while do NOT create a new scope.
    match champion:
        case Champion.samira:
            role = "ADC"
        case Champion.darius:
            role = "Top Lane"
        case Champion.leblanc:
            role = "Mid Lane"
        case _:  # Default case // I suppose you can never reach this
            role = "Unknown"

    return {"champion": champion.title(), "role": role}


# --------------------------------------------------------------------------------------------------


# File paths work with `:path`, but this wont show in the docs
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


# --------------------------------------------------------------------------------------------------
# Items 2 Additional Validaion


@app.get("/items/")
def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery\d*$")
    ] = None,
):
    results = {"items": [{"item_id": "lolol"}, {"item_id": "hehe"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/list/")
def read_item_list(
    q: Annotated[
        list[str] | None,
        Query(
            title="TITLE OF QUERY STRING",  # ka wo man den sehen soll im swaggerUI, in redoc steht es da
            description="Query string for the items to search in the database that have a good match",
            alias="item-query",  # how to call it in the URL
            deprecated=True,
            # include_in_schema=False,  # if you want to hide it from the docs
        ),
    ] = ["lolol", "hehe"]
):
    query_items = {"q": q}
    return query_items


# --------------------------------------------------------------------------------------------------


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id


@app.get("/movie/")
def get_movie(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

# --------------------------------------------------------------------------------------------------

@app.get("/path/items/{item_id}")
def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
