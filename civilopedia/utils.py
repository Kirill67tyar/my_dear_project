from django.shortcuts import get_object_or_404
from .forms import Post, tags_validator
from .models import Tag
from django.contrib import messages
from django.views import View







def validate_and_add_tags(request, fountainhead):
    tags = fountainhead['name_tag']
    tags2 = request.POST['name_tag']
    args = [] # под вопросом нужен ли этот args. Попробуй убрать.
    if tags:
        tags = tags.split('#')
        for tag in tags:
            tag = tags_validator(tag)
            if tag:
                t = Tag.objects.create(name_tag=tag)
                args.append(t)
                messages.info(request, 'теги добавлены1')
            else:
                messages.error(request, f'тег {tag} уже создан!!!')
    else:
        messages.error(request, f'тег {tags} уже создан???')
    return args



class AddOrChangePostMixin(View):
    def add_or_change_post(self, request, form):
        cd = form.cleaned_data
        work_with_post = form.save(commit=False)
        work_with_post.author = request.user

        if request.POST['direct_to'] == 'publish':
            work_with_post.is_published = True
        else:
            work_with_post.is_published = False

        work_with_post.save()
        form.save_m2m()

        if cd['name_tag']:
            post = get_object_or_404(Post, name_post=cd['name_post'])
            post.tags.add(*validate_and_add_tags(request, cd))
            post.save()



