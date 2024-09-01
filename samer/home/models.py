from bson import ObjectId

from samer.utils import MongoDBCollection, db


class ProfileInformation(MongoDBCollection):
    app_name: str
    app_real_name: str
    descriptions: list[str]
    url: str | None
    image_url: str

    def create(
        self,
        app_name: str,
        app_real_name: str,
        descriptions: list[str],
        image_url: str,
        url: str | None = None,
    ):
        profile = {
            "_id": ObjectId(),
            "app_name": app_name,
            "app_real_name": app_real_name,
            "descriptions": descriptions,
            "url": url,
            "image_url": image_url,
        }
        res = self.collection.insert_one(profile)
        return res


profile = ProfileInformation(db=db, collection_name="ProfileInformation")
