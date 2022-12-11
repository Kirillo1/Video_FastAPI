import ormar
from datetime import datetime
from db import metadata, database
from typing import Union


class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=50)


class Video(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=40)
    description: str = ormar.String(max_length=1000)
    file: str = ormar.String(max_length=1000)
    # create_at: ormar.DateTime(default=datetime.now)
    user: Union[User, int, None] = ormar.ForeignKey(User)
