from bson import ObjectId

from samer.utils import MongoDBCollection, db


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
    ):
        user = {
            '_id': ObjectId(),
            'admin': False,
            'name': None,
            'surname': None,
            'email': None,
            'username': username,
            'password': password,
        }
        res = self.insert_one(user)
        return res


user = User(db=db, collection_name='User')
