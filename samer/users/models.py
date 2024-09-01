from bson import ObjectId
from typing import TypedDict, TypeVar

from samer.utils import MongoDBCollection, db
from samer.posts.models import comment as mongo_comment
from samer.questions.models import question as mongo_question

U = TypeVar("U", bound="User")


class ParsedUser(TypedDict):
    id: str
    admin: bool
    name: str | None
    surname: str | None
    email: str | None
    username: str
    password: str


# USERNAME Y EMAIL TIENEN QUE SER UNICOS
# ADMINS TIENEN QUE TENER TODA LA INFORMACION
# USERS TIENEN QUE TENER USERNAME Y PASSWORD
class User(MongoDBCollection):
    admin: bool = False
    name: str | None
    surname: str | None
    email: str | None
    username: str
    password: str

    def create(
        self,
        username: str,
        password: str,
        admin: bool = False,
        email: str | None = None,
        name: str | None = None,
        surname: str | None = None,
    ):
        user = {
            "_id": ObjectId(),
            "admin": admin,
            "name": name,
            "surname": surname,
            "email": email,
            "username": username,
            "password": password,
        }
        res = self.insert_one(user)
        return res

    def parsed_user(self, user_id: str) -> ParsedUser | None:
        user = self.find_one({"_id": ObjectId(user_id)})
        if user is None:
            return None
        return {
            "id": str(user["_id"]),
            "admin": user["admin"],
            "name": user["name"],
            "surname": user["surname"],
            "email": user["email"],
            "username": user["username"],
            "password": user["password"],
        }

    def delete_users(self, users: list[U]):
        comments = mongo_comment.find(
            query={"author": {"$in": [str(user["_id"]) for user in users]}}
        )
        mongo_comment.delete_comments(list(comments))
        questions = mongo_question.find(
            query={"author": {"$in": [str(user["_id"]) for user in users]}}
        )
        mongo_question.delete_questions(list(questions))
        self.collection.delete_many(
            {"_id": {"$in": [user["_id"] for user in users]}},
        )


user = User(db=db, collection_name="User")
