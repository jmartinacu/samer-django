from datetime import datetime

from bson import ObjectId

from samer.utils import db
from samer.users.hashing import hash_password

posts_data = [
    {
        '_id': ObjectId(),
        'name': 'montañas_carretera',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1511765224389-37f0e77cf0eb?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'familia_lago',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1497445462247-4330a224fdb1?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'montañas_arboles',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'gaviota_puente',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1502630859934-b3b41d18206c?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'hamburguesa_persona',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1498471731312-b6d2b8280c61?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'sandia_persona',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1515023115689-589c33041d3c?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'lago_canoas',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'perro_mochila',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1515814472071-4d632dbc5d4a?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'coche_calle',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1511407397940-d57f68e81203?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'libro_mesa',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1518481612222-68bbe828ecd1?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'guitarra_persona',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1505058707965-09a4469a87e4?w=500&h=500&fit=crop',
        'likes': []
    },
    {
        '_id': ObjectId(),
        'name': 'playa_skate',
        'object_name': None,
        'url': 'https://images.unsplash.com/photo-1423012373122-fff0a5d28cc9?w=500&h=500&fit=crop',
        'likes': []
    },
]

users_data = [
    {
        '_id': ObjectId(),
        'admin': False,
        'name': None,
        'surname': None,
        'email': None,
        'username': 'joaquin',
        'password': hash_password('123qwe')
    },
    {
        '_id': ObjectId(),
        'admin': True,
        'name': 'admin',
        'surname': 'admin',
        'email': 'admin@admin.com',
        'username': 'admin',
        'password': hash_password('admin123')
    },
]

comments_data = [
    {
        '_id': ObjectId(),
        'post': str(posts_data[0]['_id']),
        'author': str(users_data[0]['_id']),
        'created_at': datetime.now(),
        'text': 'He sido el primero',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[0]['_id']),
        'author': str(users_data[1]['_id']),
        'created_at': datetime.now(),
        'text': 'Una foto muy bonita',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[0]['_id']),
        'author': str(users_data[0]['_id']),
        'created_at': datetime.now(),
        'text': 'Me gusta la luz que tiene',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[1]['_id']),
        'author': str(users_data[1]['_id']),
        'created_at': datetime.now(),
        'text': 'He sido el primero en comentar',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[2]['_id']),
        'author': str(users_data[1]['_id']),
        'created_at': datetime.now(),
        'text': 'Quien ha hecho la foto?',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[2]['_id']),
        'author': str(users_data[0]['_id']),
        'created_at': datetime.now(),
        'text': 'Me encanta como se refleja la luz del sol en la montaña!!',
    },
    {
        '_id': ObjectId(),
        'post': str(posts_data[2]['_id']),
        'author': str(users_data[1]['_id']),
        'created_at': datetime.now(),
        'text': 'Ojala poder visitar ese lugar',
    },
]


def populate_posts():
    collection = db['Post']
    collection.drop()
    collection.insert_many(posts_data)


def populate_users():
    collection = db['User']
    collection.drop()
    collection.insert_many(users_data)


def populate_comments():
    collection = db['Comment']
    collection.drop()
    collection.insert_many(comments_data)


def populate():
    populate_posts()
    populate_users()
    populate_comments()


populate()
