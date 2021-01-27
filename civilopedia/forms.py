from django import forms
from django.utils.html import format_html
from .models import Tag, Category, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


tag = '<i class="fa fa-picture-o" aria-hidden="true"></i>'


# def image_for_file():
#     return format_html('<i class="fa fa-picture-o" aria-hidden="true"></i>')


# функция возвращает тэг, или значение None, если тэг не валидный
def tags_validator(tag):
    tag = tag.lstrip().rstrip()
    if tag.startswith('#'):
        tag = tag[1:]
    if tag.endswith('#'):
        tag = tag[:-1]
    tag = tag.lstrip().rstrip()
    if not Tag.objects.filter(name_tag=tag.lower()).exists():
        return tag
    return None


class PostForm(forms.ModelForm):
    name_tag = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',}))
    is_published = False

    class Meta:
        model = Post
        fields = 'name_post', 'content',  'photo', 'category', 'tags','is_published', 'name_tag'
        widgets = {
            'name_post' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название статьи'}),
            'content': CKEditorUploadingWidget(),

            'category': forms.Select(attrs={'class': 'form-control',}),
            'tags': forms.SelectMultiple(),
            'photo': forms.FileInput(attrs={'class': "form-control-file",}),
            # 'is_published': forms.CheckboxInput(attrs={'class': 'form-control',}),
        }

    def clean_name_tag(self):
        return tags_validator(self.cleaned_data['name_tag'])
    # использовать валидатор, проверяющий нет ли поста с таким названием
    # def clean_tags


class TagForm(forms.Form):

    name_tag = forms.CharField(
        label='Добавляйте тэги через "#" без пробела. Внутри тега между словами пробел ставить можно.',
        widget=forms.TextInput(attrs={'class': 'form-control',}),
        validators=[tags_validator,])
#     использовать при добавлении слага - валидаторы проверяющие нет ли там ?!@#@#!$$%#%



