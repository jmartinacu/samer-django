from datetime import datetime

from bson import ObjectId

from samer.utils import MongoDBCollection, db


class Post(MongoDBCollection):
    name: str
    object_name: str | None
    url: str
    likes: list[str]

    def create(self, name: str, object_name: str, url: str):
        post = {
            '_id': ObjectId(),
            'name': name,
            'object_name': object_name,
            'url': url,
            'likes': [],
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
