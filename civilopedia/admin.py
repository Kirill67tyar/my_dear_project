from django.contrib import admin
from django import template
from django.utils.safestring import mark_safe
from .models import Tag, Category, Post, FunFact
from mptt.admin import DraggableMPTTAdmin



register = template.Library()




# PF = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    readonly_fields = 'slug',
    search_fields = 'name_tag', 'slug',

    # prepopulated_fields = PF


class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):

    # prepopulated_fields = PF

    list_display = 'tree_actions', 'indented_title', 'id', 'name_category',

    list_display_links = 'indented_title',

    readonly_fields = 'slug',



class PostAdmin(admin.ModelAdmin):
    # prepopulated_fields = PF  # prepopulated_fields позволяет автоматически вводить поле привязанное к значению
    save_on_top = True  # распологает панель сохранения и на верху (не убирает внизу)
    # form = PostAdminForm  # это для особого поля ввода, в данном лучае панель инструментов CKEditor
    save_as = True  #
    list_display = 'id', 'name_post', 'slug', 'category', 'get_photo', 'views', #, 'created'
    list_display_links = 'id', 'name_post',
    search_fields = 'name_post', 'content'
    list_filter = 'category', 'tags',
    readonly_fields = 'created', 'get_photo', 'slug', 'author',
    fields = 'author', 'name_post', 'slug', 'category', 'tags', 'content',\
             'photo', 'views', 'is_published', 'created', 'get_photo',

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '--/--'

    get_photo.short_description = 'Фото'



class FunFactAdmin(admin.ModelAdmin):

    fields = 'fact',

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(FunFact, FunFactAdmin)



