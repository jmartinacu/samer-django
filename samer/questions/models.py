from typing import TypedDict, TypeVar, Union

from bson import ObjectId

from samer.utils import MongoDBCollection, db

Q = TypeVar("Q", bound="Question")


class AnswerQuestion(TypedDict):
    text: str
    admin: str


class ParsedQuestion(TypedDict):
    id: str | ObjectId
    title: str
    content: str
    author: str
    resolve: bool
    archive: bool
    answer: Union[AnswerQuestion, None]
    likes: list[str]
    tags: list[str]
    views: list[str]


class Question(MongoDBCollection):
    title: str
    content: str
    author: str
    resolve: bool
    archive: bool
    answer: Union[AnswerQuestion, None]
    likes: list[str]
    tags: list[str]
    views: list[str]

    def create(
        self,
        title: str,
        content: str,
        author: str,
        resolve: bool = False,
        archive: bool = False,
        answer: Union[AnswerQuestion, None] = None,
        likes: list[str] = [],
        tags: list[str] = [],
        views: list[str] = [],
    ):
        question = {
            "_id": ObjectId(),
            "title": title,
            "content": content,
            "author": author,
            "resolve": resolve,
            "archive": archive,
            "answer": answer,
            "likes": likes,
            "tags": tags,
            "views": views,
        }
        res = self.collection.insert_one(question)
        return res

    def parse_question(
        self,
        question_id: str,
    ) -> Union[ParsedQuestion, None]:
        question = self.collection.find_one({"_id": ObjectId(question_id)})
        if question is None:
            return None
        return {
            "id": str(question["_id"]),
            "title": question["title"],
            "content": question["content"],
            "author": question["author"],
            "resolve": question["resolve"],
            "archive": question["archive"],
            "answer": question["answer"],
            "likes": question["likes"],
            "tags": question["tags"],
            "views": question["views"],
        }

    def get_questions_sorted_by_likes(
        self,
        query: dict = {},
        archive: bool = False,
    ) -> list[Q]:
        query["archive"] = archive
        return list(
            self.collection.aggregate(
                [
                    {"$match": query},
                    {"$addFields": {"likes_length": {"$size": "$likes"}}},
                    {"$sort": {"likes_length": -1}},
                ]
            )
        )

    def add_or_remove_likes(self, question: Q, user_ids: list[str]):
        users_already_like = [u for u in user_ids if u in question["likes"]]
        users_like = list(set(user_ids).difference(set(users_already_like)))
        self.update_one(
            filter={"_id": question["_id"]},
            update={"$set": {"likes": users_like}},
        )

    def add_view(self, question: Q | ParsedQuestion, user_id: str):
        question_id = (
            ObjectId(
                question["id"],
            )
            if "id" in question
            else question["_id"]
        )
        views = question["likes"] + [user_id]
        self.update_one(
            filter={"_id": question_id},
            update={
                "$set": {"views": views},
            },
        )
        return views

    def add_answer(self, question_id: str, answer: AnswerQuestion):
        self.update_one(
            filter={"_id": ObjectId(question_id)},
            update={
                "$set": {
                    "answer": answer,
                    "resolve": True,
                }
            },
        )

    def delete_questions(self, questions: list[Q]):
        self.collection.delete_many(
            {"_id": {"$in": [question["_id"] for question in questions]}},
        )

    def archive_unarchive_questions(self, questions: list[str]):
        questions = list(
            self.find(
                query={"_id": {"$in": list(map(ObjectId, questions))}},
            )
        )
        archive_question = [q["_id"] for q in questions if q["archive"]]
        unarchive_question = [q["_id"] for q in questions if not q["archive"]]
        if len(unarchive_question) != 0:
            self.update_many(
                filter={"_id": {"$in": unarchive_question}},
                update={"$set": {"archive": True}},
            )
        if len(archive_question) != 0:
            self.update_many(
                filter={"_id": {"$in": archive_question}},
                update={"$set": {"archive": False}},
            )

    def get_unresolved(self, username: str, archive: bool = False) -> list[Q]:
        return list(
            self.find(
                query={
                    "resolve": False,
                    "archive": archive,
                    "author": username,
                },
            )
        )


question = Question(db=db, collection_name="Question")
