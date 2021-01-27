from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from civilopedia.models import Post, Tag, Category, FunFact
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView


# s = get_object_or_404()


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'username', #'email'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'id', 'name_category', 'slug',


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id', 'name_tag', 'slug',


class PostSerializer(serializers.ModelSerializer): # or serializers.HyperlinkedModelSerializer
    author = AuthorSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = 'id', 'name_post', 'slug', 'author', 'created', \
                 'updated', 'views', 'is_published', 'category', 'tags',








""" name_post         = models.CharField(max_length=250, verbose_name='Наименование статьи')
    slug         = models.SlugField(max_length=250, unique=True, verbose_name='Url_статьи')
    content      = RichTextUploadingField(blank=True, verbose_name='Контент')
    # content      = models.TextField(blank=True, verbose_name='Контент')
    created      = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated      = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    photo        = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    category     = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags         = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Тэги')
    views        = models.IntegerField(default=0, verbose_name='Просмотры')
    """