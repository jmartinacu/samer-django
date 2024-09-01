from enum import Enum
from datetime import datetime
from typing import Literal, Union, TypedDict, TypeVar

from bson import ObjectId

from samer.utils import MongoDBCollection, db, delete_file

P = TypeVar("P", bound="Post")
C = TypeVar("C", bound="Comment")
T = TypeVar("T", bound="Tag")


class PostTypes(Enum):
    IMAGE = "image"
    VIDEO = "video"


class ParsedPost(TypedDict):
    id: str
    name: str
    object_names: list[str] | None
    urls: list[str]
    thumbnail_url: str | None
    likes: list[str]
    description: str | None
    type: Literal["image", "video"]


class ParsedComment(TypedDict):
    id: str | ObjectId
    post: str
    author: str
    created_at: datetime
    text: str


class ParsedTag(TypedDict):
    id: str | ObjectId
    name: str
    posts: list[str]
    object_name: str
    url: str


class Comment(MongoDBCollection):
    post: str
    author: str
    created_at: datetime
    text: str

    def create(self, post: str, author: str, text: str):
        comment = {
            "_id": ObjectId(),
            "post": post,
            "author": author,
            "text": text,
            "created_at": datetime.now(),
        }
        res = self.collection.insert_one(comment)
        return res

    def delete_comments(self, comments: list[C]):
        self.collection.delete_many(
            {"_id": {"$in": [comment["_id"] for comment in comments]}},
        )


comment = Comment(db=db, collection_name="Comment")


class Tag(MongoDBCollection):
    name: str
    posts: list[str]
    object_name: str
    url: str

    def create(
        self,
        name: str,
        object_name: str,
        url: str,
        posts: list[str] = [],
    ):
        tag = {
            "_id": ObjectId(),
            "name": name,
            "posts": posts,
            "object_name": object_name,
            "url": url,
        }
        res = self.collection.insert_one(tag)
        return res

    def parse_tag(
        self,
        tag_id: str,
    ) -> Union[ParsedTag, None]:
        tag = self.collection.find_one({"_id": ObjectId(tag_id)})
        if tag is None:
            return None
        return {
            "id": str(tag["_id"]),
            "name": tag["name"],
            "posts": tag["posts"],
            "object_name": tag["object_name"],
            "url": tag["url"],
        }

    def add_posts(self, tag: T, post_ids: list[str]):
        if any(post_id in tag["posts"] for post_id in post_ids):
            raise ValueError("Post already in tag")
        self.update_one(
            filter={"_id": tag["_id"]},
            update={"$set": {"posts": tag["posts"] + post_ids}},
        )

    def delete_tags(self, tags: list[T]):
        for tag in tags:
            delete_file(object_name=tag["object_name"])
        self.collection.delete_many(
            {"_id": {"$in": [tag["_id"] for tag in tags]}},
        )


tag = Tag(db=db, collection_name="Tag")


class Post(MongoDBCollection):
    name: str
    object_names: list[str] | None
    urls: list[str]
    thumbnail_url: str | None
    likes: list[str]
    description: str | None
    type: PostTypes

    def create(
        self,
        name: str,
        description: str | None,
        type: PostTypes,
        object_names: list[str] = [],
        urls: list[str] = [],
        thumbnail_url: str | None = None,
    ):
        post = {
            "_id": ObjectId(),
            "name": name,
            "object_names": object_names,
            "urls": urls,
            "thumbnail_url": thumbnail_url,
            "likes": [],
            "description": description,
            "type": type.value,
        }
        res = self.collection.insert_one(post)
        return res

    def parse_post(
        self,
        post_id: str,
    ) -> Union[ParsedPost, None]:
        post = self.collection.find_one({"_id": ObjectId(post_id)})
        if post is None:
            return None
        return {
            "id": str(post["_id"]),
            "name": post["name"],
            "object_names": post["object_names"],
            "urls": post["urls"],
            "thumbnail_url": post["thumbnail_url"],
            "likes": post["likes"],
            "description": post["description"],
            "type": post["type"],
        }

    def delete_posts(self, posts: list[P]):
        for post in posts:
            if post["object_names"] is None:
                continue
            for object_name in post["object_names"]:
                delete_file(object_name=object_name)
        post_ids = [str(post["_id"]) for post in posts]
        comment.delete_comments(
            list(
                comment.find(
                    query={
                        "post": {"$in": post_ids},
                    },
                )
            ),
        )
        tags_db = list(tag.find({"posts": {"$in": post_ids}}))
        for t in tags_db:
            new_posts = [p for p in t["posts"] if p not in post_ids]
            tag.update_one(
                filter={"_id": t["_id"]},
                update={"$set": {"posts": new_posts}},
            )
        self.collection.delete_many(
            {"_id": {"$in": [post["_id"] for post in posts]}},
        )


post = Post(db=db, collection_name="Post")
