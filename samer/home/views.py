from django.shortcuts import render

from samer.posts.models import post as mongo_post, comment as mongo_comment


def home(request):
    posts = [
        {
            'id': str(post['_id']),
            'name': post['name'],
            'url': post['url'],
            'comments': mongo_comment.count(query={'post': str(post['_id'])}),
            'likes': post['likes']
        }
        for post in mongo_post.find(query={})
    ]
    return render(request, 'home/home.html', {
        'posts': posts
    })
