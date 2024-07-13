from django.shortcuts import render

from samer.posts.models import post as mongo_post, comment as mongo_comment


def home_images(request):
    posts = [
        {
            'id': str(post['_id']),
            'name': post['name'],
            'url': post['url'],
            'comments': mongo_comment.count(query={'post': str(post['_id'])}),
            'likes': post['likes'],
            'description': post['description'],
            'type': post['type'],
        }
        for post in mongo_post.find(query={'type': 'image'})
    ]
    return render(request, 'home/images.html', {
        'posts': posts
    })


def home_videos(request):
    posts = [
        {
            'id': str(post['_id']),
            'name': post['name'],
            'thumbnail_url': post['thumbnail_url'],
            'comments': mongo_comment.count(query={'post': str(post['_id'])}),
            'likes': post['likes'],
            'description': post['description'],
            'type': post['type'],
        }
        for post in mongo_post.find(query={'type': 'video'})
    ]
    return render(request, 'home/videos.html', {
        'posts': posts
    })
