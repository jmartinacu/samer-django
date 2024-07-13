from enum import Enum
from datetime import datetime

from bson import ObjectId

from samer.utils import MongoDBCollection, db


class PostTypes(Enum):
    IMAGE = 'image'
    VIDEO = 'video'


class Post(MongoDBCollection):
    name: str
    object_name: str | None
    url: str
    thumbnail_url: str | None
    likes: list[str]
    description: str | None
    type: PostTypes

    def create(
        self, name: str, object_name: str,
        url: str, description: str | None,
        type: PostTypes, thumbnail_url: str | None = None
    ):
        post = {
            '_id': ObjectId(),
            'name': name,
            'object_name': object_name,
            'url': url,
            'thumbnail_url': thumbnail_url,
            'likes': [],
            'description': description,
            'type': type.value,
        }
        res = self.collection.insert_one(post)
        return res


class Comment(MongoDBCollection):
    post: str
    author: str
    created_at: datetime
    text: str

    def create(self, post: str, author: str, text: str):
        comment = {
            '_id': ObjectId(),
            'post': post,
            'author': author,
            'text': text,
            'created_at': datetime.now(),
        }
        res = self.collection.insert_one(comment)
        return res


post = Post(db=db, collection_name='Post')
comment = Comment(db=db, collection_name='Comment')
