from django.shortcuts import render, redirect
from django.urls import reverse
from bson import ObjectId

from samer.posts.forms import CreateCommentForm
from samer.posts.models import (
    Post,
    post as mongo_post,
    comment as mongo_comment
)
from samer.users.context_processors import UserAuth


def add_remove_like(request, post_id):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        # LANZAR ERROR NO AUTORIZADO
        return redirect(reverse('home:home_images'))
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
    return redirect(reverse('home:home_images'))


def comments(request, post_id: str):
    user_auth = UserAuth(request)
    if request.method == 'POST':
        if not user_auth.is_login():
            # LANZAR ERROR QUE NO ESTA AUTORIZADO
            return redirect(reverse('home:home_images'))
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            author = user_auth.user_auth['id']
            mongo_comment.create(post_id, author, comment)
            post_db = mongo_post.find_one(query={'_id': ObjectId(post_id)})
            if post_db is None:
                # DEBERIA DE LANZAR UN ERROR AL USUARIO
                return redirect(reverse('home:home_images'))
            post = {
                'id': str(post_db['_id']),
                'name': post_db['name'],
                'url': post_db['url'],
                'comments': mongo_comment.count(query={'post': str(post_db['_id'])}),
                'likes': post_db['likes'],
                'description': post_db['description'],
                'type': post_db['type'],
            }
            comments = mongo_comment.find(query={'post': post_id})
            comment_form = CreateCommentForm()
            return render(request, 'posts/comment.html', {
                'post': post,
                'comments': [
                    {
                        'id': str(comment['_id']),
                        'post': comment['post'],
                        'author': comment['author'],
                        'created_at': comment['created_at'],
                        'text': comment['text'],
                    }
                    for comment in comments
                ],
                'form': comment_form,
            })
    else:
        post_db = mongo_post.find_one(query={'_id': ObjectId(post_id)})
        if post_db is None:
            # DEBERIA DE LANZAR UN ERROR AL USUARIO
            return redirect(reverse('home:home_images'))
        post = {
            'id': str(post_db['_id']),
            'name': post_db['name'],
            'url': post_db['url'],
            'comments': mongo_comment.count(query={'post': str(post_db['_id'])}),
            'likes': post_db['likes'],
            'description': post_db['description'],
            'type': post_db['type'],
        }
        comment_form = CreateCommentForm()
        comments = mongo_comment.find(query={'post': post_id})
        return render(request, 'posts/comment.html', {
            'post': post,
            'comments': [
                {
                    'id': str(comment['_id']),
                    'post': comment['post'],
                    'author': comment['author'],
                    'created_at': comment['created_at'],
                    'text': comment['text'],
                }
                for comment in comments
            ],
            'form': comment_form,
        })


def remove_comment(request, post_id: str, comment_id: str):
    user_auth = UserAuth(request)
    if not user_auth.is_login():
        # LANZAR ERROR NO AUTORIZADO
        return redirect(reverse('home:home_images'))
    comment_db = mongo_comment.find_one({'_id': ObjectId(comment_id)})
    post_db = mongo_post.find_one(query={'_id': ObjectId(post_id)})
    if post_db is None:
        # DEBERIA DE LANZAR UN ERROR AL USUARIO
        return redirect(reverse('home:home_images'))
    if comment_db is None:
        # LANZAR ERROR NO ENCONTRADO
        return redirect(reverse('posts:comment', args=[post_id]))
    if not comment_db['author'] == user_auth.user_auth['id']:
        # LANZAR ERROR NO AUTORIZADO
        return redirect(reverse('home:home_images'))
    mongo_comment.delete_one({'_id': ObjectId(comment_id)})
    post = {
        'id': str(post_db['_id']),
        'name': post_db['name'],
        'url': post_db['url'],
        'comments': mongo_comment.count(query={'post': str(post_db['_id'])}),
        'likes': post_db['likes'],
        'description': post_db['description'],
        'type': post_db['type'],
    }
    comment_form = CreateCommentForm()
    comments = mongo_comment.find(query={'post': post_id})
    return render(request, 'posts/comment.html', {
        'post': post,
        'comments': [
            {
                'id': str(comment['_id']),
                'post': comment['post'],
                'author': comment['author'],
                'created_at': comment['created_at'],
                'text': comment['text'],
            }
            for comment in comments
        ],
        'form': comment_form,
    })
