from django import template
from civilopedia.models import Tag, Post, FunFact, Category
from django.db.models import Count
from random import choice

from django.shortcuts import get_object_or_404

register = template.Library()

@register.inclusion_tag('civilopedia/my_tags/tags_cloud.html')
def get_tags_cloud(count_tags=7, col_lg=4):

    tags = []
    for tag in Tag.objects.annotate(cnt=Count('posts')):
        tags.append({'name':tag, 'cnt':tag.cnt})

    # Можно отсеивать на сервере:
    # tags.sort(key=lambda x: x['cnt'], reverse=True)
    # tags = tags[:count_tags]

    # а можно в шаблоне (смотри на фильтр dictsortreversed)

    # если отсеишь на сервере, то убери  |dictsortreversed:'cnt' из шаблона

    return {'tags': tags, 'count_tags': count_tags, 'col_lg': col_lg,}



@register.inclusion_tag('civilopedia/my_tags/popular_and_latest_posts.html')
def get_popular_and_latest_posts(count_posts=5, count_words=5):
    popular_posts = Post.objects.order_by('-views')[:count_posts]
    latest_posts = Post.objects.order_by('-created')[:count_posts]
    context = {
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'count_posts': count_posts,
        'count_words': count_words,
    }
    print(f'\n\n**************************************\n\n'
          f'popular_posts - {popular_posts}\n\n'
          f'latest_posts - {latest_posts}\n\n'
          f'\n\n**************************************\n\n')
    return context



@register.inclusion_tag('civilopedia/my_tags/fun_fact.html')
def get_fun_fact():
    fact = choice(FunFact.objects.all())
    return {'fact': fact}



@register.simple_tag(name='get_title')
def get_title(slug, filter):
    context = {}
    k = 'key'
    v = 'filter'
    if filter is 'tag':
        context[k] = get_object_or_404(Tag, slug=slug).name_tag
        context[v] = 'тегу'
    elif filter is 'category':
        context[k] = get_object_or_404(Category, slug=slug).name_category
        context[v] = 'категории'
    return f'Все статьи{f" по {context[v]} {repr(context[k])}" if filter else ""}'

