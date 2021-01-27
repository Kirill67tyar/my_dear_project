from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from slugify import slugify
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from ckeditor_uploader.fields import RichTextUploadingField





class Tag(models.Model):
    name_tag = models.CharField(max_length=100, verbose_name='Наименование тэга')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Url_тега')

    def get_absolute_url(self):
        return reverse('civilopedia:posts_by_tag', kwargs={'tag': self.slug})

    def __str__(self):
        return self.name_tag



    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_tag,  to_lower=True)
        self.name_tag = self.name_tag.lower()
        return super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = 'name_tag',



class Category(MPTTModel):
    name_category = models.CharField(max_length=200, db_index=True, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Url_категории')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='Children', verbose_name='Подкатегории')

    def get_absolute_url(self):
        return reverse('civilopedia:posts_by_category', kwargs={'category': self.slug})

    def __str__(self):
        return self.name_category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_category,  to_lower=True)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'




class Post(models.Model):
    name_post         = models.CharField(max_length=250, verbose_name='Наименование статьи')
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

    # допишем, когда будем делать авторизацию и регистрацию
    author       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    # подумать над полем рейтинг (возможно оно будет связано с сигналами)

    def get_absolute_url(self):
        return reverse('civilopedia:view_post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name_post

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name_post,  to_lower=True)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'



class FunFact(models.Model):
    name_fact = models.CharField(max_length=200, verbose_name='факты')

    class Meta:
        verbose_name = 'Факт'
        verbose_name_plural = 'Факты'
        ordering = 'name_fact',



class Token(models.Model):
    token = models.CharField(max_length=100, verbose_name='Токен')

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
