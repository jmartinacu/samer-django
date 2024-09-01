import os
from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

from samer.users.hashing import hash_password
from samer.posts.utils import upload_thumbnail

load_dotenv()

client = MongoClient(os.environ["CONNECTION_STRING"])
db = client[os.environ["DB_NAME"]]


posts_data = [
    {
        "_id": ObjectId(),
        "name": "montañas_carretera",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1511765224389-37f0e77cf0eb?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8",
            "https://images.unsplash.com/photo-1494597564530-871f2b93ac55",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "familia_lago",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1497445462247-4330a224fdb1?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": None,
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "montañas_arboles",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "gaviota_puente",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1502630859934-b3b41d18206c?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "hamburguesa_persona",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1498471731312-b6d2b8280c61?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Integer in mauris eu nibh euismod gravida.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "sandia_persona",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1515023115689-589c33041d3c?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "lago_canoas",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Maecenas fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla a mi.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "perro_mochila",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1515814472071-4d632dbc5d4a?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "coche_calle",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1511407397940-d57f68e81203?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": None,
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "libro_mesa",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1518481612222-68bbe828ecd1?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": "Cras mollis scelerisque nunc. Nullam arcu. Aliquam consequat. Curabitur augue lorem, dapibus quis, laoreet et, pretium ac, nisi. Aenean magna nisl, mollis quis, molestie eu, feugiat in, orci. In hac habitasse platea dictumst.",
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "guitarra_persona",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1505058707965-09a4469a87e4?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": None,
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "playa_skate",
        "object_names": [],
        "urls": [
            "https://images.unsplash.com/photo-1423012373122-fff0a5d28cc9?w=500&h=500&fit=crop",
        ],
        "thumbnail_url": None,
        "likes": [],
        "description": None,
        "type": "image",
    },
    {
        "_id": ObjectId(),
        "name": "caballo",
        "object_names": ["videos/caballo.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/caballo.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/caballo.mp4"
        ),
        "likes": [],
        "description": "Video de un caballo",
        "type": "video",
    },
    {
        "_id": ObjectId(),
        "name": "escalera",
        "object_names": ["videos/escalera.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/escalera.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/escalera.mp4"
        ),
        "likes": [],
        "description": None,
        "type": "video",
    },
    {
        "_id": ObjectId(),
        "name": "kanguro",
        "object_names": ["videos/kanguro.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/kanguro.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/kanguro.mp4"
        ),
        "likes": [],
        "description": "Video de un kanguro",
        "type": "video",
    },
    {
        "_id": ObjectId(),
        "name": "montana",
        "object_names": ["videos/montana.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/montana.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/montana.mp4"
        ),
        "likes": [],
        "description": "Video montaña",
        "type": "video",
    },
    {
        "_id": ObjectId(),
        "name": "playa",
        "object_names": ["videos/playa.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/playa.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/playa.mp4"
        ),
        "likes": [],
        "description": None,
        "type": "video",
    },
    {
        "_id": ObjectId(),
        "name": "ventana",
        "object_names": ["videos/ventana.mp4"],
        "urls": [
            "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/ventana.mp4",
        ],
        "thumbnail_url": upload_thumbnail(
            0, "https://samerbucket2.s3.eu-central-1.amazonaws.com/videos/ventana.mp4"
        ),
        "likes": [],
        "description": None,
        "type": "video",
    },
]

users_data = [
    {
        "_id": ObjectId(),
        "admin": True,
        "name": "admin",
        "surname": "admin",
        "email": "admin@admin.com",
        "username": "admin",
        "password": hash_password("le`2YlIM!P!:1PWo5D+`)Nw^"),
    },
    {
        "_id": ObjectId(),
        "admin": False,
        "name": None,
        "surname": None,
        "email": None,
        "username": "jmartinacu",
        "password": hash_password("nNnZ0_=RrNXFV43yA.p6VYkK"),
    },
]

comments_data = [
    {
        "_id": ObjectId(),
        "post": str(posts_data[0]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "He sido el primero",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[0]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "Una foto muy bonita",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[0]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "Me gusta la luz que tiene",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[1]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "He sido el primero en comentar",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[2]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "Quien ha hecho la foto?",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[2]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "Me encanta como se refleja la luz del sol en la montaña!!",
    },
    {
        "_id": ObjectId(),
        "post": str(posts_data[2]["_id"]),
        "author": str(users_data[0]["_id"]),
        "created_at": datetime.now(),
        "text": "Ojala poder visitar ese lugar",
    },
]

profile_data = [
    {
        "_id": ObjectId(),
        "app_name": "samervalme",
        "app_real_name": "Salud Mental En Red - SAMER Valme\n",
        "descriptions": [
            "💫 Programa de Prevención y Promoción de la Salud Mental ❤️🧠",
            "🏥 Área Sur de Sevilla - Hospital de Valme",
            "🌾 Creamos recursos y contenidos En Red.",
        ],
        "url": "https://www.agssursevilla.org/",
        "image_url": "https://samerbucket2.s3.eu-central-1.amazonaws.com/samerlogo.jpg",
    }
]

tags_data = [
    {
        "_id": ObjectId(),
        "name": "Comida",
        "url": "https://samerbucket2.s3.eu-central-1.amazonaws.com/tags/bol.jpeg",
        "object_name": "tags/bol.jpeg",
        "posts": [
            str(posts_data[0]["_id"]),
            str(posts_data[1]["_id"]),
            str(posts_data[2]["_id"]),
        ],
    },
    {
        "_id": ObjectId(),
        "name": "Diversión",
        "url": "https://samerbucket2.s3.eu-central-1.amazonaws.com/tags/globos.jpeg",
        "object_name": "tags/globos.jpeg",
        "posts": [
            str(posts_data[-1]["_id"]),
            str(posts_data[-2]["_id"]),
            str(posts_data[7]["_id"]),
        ],
    },
]

questions_data = [
    {
        "_id": ObjectId(),
        "title": "Hábitos saludables",
        "content": "¿Qué puedo hacer para mejorar mis hábitos saludables al levantarme?",
        "author": users_data[1]["username"],
        "resolve": True,
        "archive": False,
        "answer": {
            "admin": users_data[0]["username"],
            "text": "Hay varias maneras de mejorar los hábitos saludables, una de ellas es hacer ejercicio, para exponerte a la luz del sol y que tu cuerpo se active. También puedes abstenerte de tomar café en las dos primeras horas de la mañana para que tu cuerpo recupere su ciclo normal naturalmente.",
        },
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Aprender un nuevo idioma",
        "content": "¿Cuáles son las mejores formas de aprender un nuevo idioma de manera efectiva?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Gestión del tiempo",
        "content": "¿Cómo puedo gestionar mejor mi tiempo durante el día?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Recetas de cocina",
        "content": "¿Qué recetas rápidas y saludables puedo preparar para la cena?",
        "author": users_data[1]["username"],
        "resolve": True,
        "archive": False,
        "answer": {
            "admin": users_data[0]["username"],
            "text": "Puedes preparar ensaladas con proteínas como pollo a la parrilla, tofu o atún. También, recetas de salteados con verduras y arroz integral son rápidas y saludables.",
        },
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Mejorar el sueño",
        "content": "¿Qué consejos puedes dar para mejorar la calidad del sueño?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Ejercicio en casa",
        "content": "¿Qué tipo de ejercicios puedo hacer en casa sin equipo?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Desarrollo personal",
        "content": "¿Cómo puedo empezar a trabajar en mi desarrollo personal?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Manejo del estrés",
        "content": "¿Qué técnicas efectivas hay para manejar el estrés?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Planificación financiera",
        "content": "¿Cómo puedo empezar a planificar mi presupuesto personal?",
        "author": users_data[1]["username"],
        "resolve": False,
        "archive": False,
        "answer": None,
        "likes": [],
    },
    {
        "_id": ObjectId(),
        "title": "Cuidado de plantas",
        "content": "¿Cuáles son los cuidados básicos para mantener una planta de interior saludable?",
        "author": users_data[1]["username"],
        "resolve": True,
        "archive": False,
        "answer": {
            "admin": users_data[0]["username"],
            "text": "Asegúrate de que tu planta reciba la cantidad adecuada de luz, agua y nutrientes. Investiga las necesidades específicas de cada tipo de planta y ajusta su cuidado en consecuencia.",
        },
        "likes": [],
    },
]


def populate_posts():
    collection = db["Post"]
    collection.drop()
    collection.insert_many(posts_data)


def populate_users():
    collection = db["User"]
    collection.drop()
    collection.insert_many(users_data)


def populate_comments():
    collection = db["Comment"]
    collection.drop()
    collection.insert_many(comments_data)


def populate_profile():
    collection = db["ProfileInformation"]
    collection.drop()
    collection.insert_many(profile_data)


def populate_tags():
    collection = db["Tag"]
    collection.drop()
    collection.insert_many(tags_data)


def populate_questions():
    collection = db["Question"]
    collection.drop()
    collection.insert_many(questions_data)


def populate():
    populate_posts()
    populate_users()
    populate_comments()
    populate_profile()
    populate_tags()
    populate_questions()


populate()
