from django.shortcuts import render, redirect
from django.urls import reverse
from bson import ObjectId

from samer.posts.models import (
    Post,
    post as mongo_post,
    comment as mongo_comment
)
from samer.users.context_processors import UserAuth


def add_remove_like(request, post_id):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        return redirect(reverse('home:home'))
    post: Post | None = mongo_post.find_one(query={'_id': ObjectId(post_id)})
    if post is None:
        # EN VEZ DE UN ERROR PODRIA SOLTAR UN WARNING EN LA PANTALLA
        return render(request, 'home/home.html', {
            'error': 'Post not found'
        })
    if user_auth.user_auth['id'] in post['likes']:
        mongo_post.update_one(
            query={'_id': ObjectId(post_id)},
            update={'$set': {'likes': [
                like for like in post['likes']
                if like != user_auth.user_auth['id']
            ]}}
        )
    else:
        mongo_post.update_one(
            query={'_id': ObjectId(post_id)},
            update={'$set': {
                'likes': post['likes'] + [user_auth.user_auth['id']]
            }}
        )
    return redirect(reverse('home:home'))


def comments(request, post_id: str):
    post = mongo_post.find_one(query={'_id': ObjectId(post_id)})
    if post is None:
        # DEBERIA DE LANZAR UN ERROR AL USUARIO
        return redirect(reverse('home:home'))
    comments = mongo_comment.find(query={'post': post_id})
    return render(request, 'posts/comment.html', {
        'post': post,
        'comments': list(comments),
    })
