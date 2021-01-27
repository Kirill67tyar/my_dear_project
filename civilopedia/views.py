from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import render, redirect, HttpResponse
from string import printable
from random import randrange, choice
from .utils import AddOrChangePostMixin, validate_and_add_tags
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category, Token
from .forms import PostForm, TagForm
from django.contrib import messages
from django.http import JsonResponse
from string import printable
from random import choice, randrange


class ListPosts(ListView):
    model = Post
    template_name = 'civilopedia/index.html'
    paginate_by = 4
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True)
    allow_empty = False


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListPosts, self).get_context_data(**kwargs)
        context['filter'] = None
        context['slug'] = None

        return context




class ListPostsByTagOrCategory(ListView):

    template_name = 'civilopedia/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = True


    def get_queryset(self):
        if 'tag' in self.kwargs:
            queryset = Post.objects.filter(tags__slug=self.kwargs['tag'], is_published=True)
        elif 'category' in self.kwargs:
            queryset = Post.objects.filter(category__slug=self.kwargs['category'], is_published=True).select_related('category')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListPostsByTagOrCategory, self).get_context_data(**kwargs)
        if 'tag' in self.kwargs or 'category' in self.kwargs:
            if 'tag' in self.kwargs:
                filter = 'tag'
                slug = self.kwargs['tag']
            else:
                filter = 'category'
                slug = self.kwargs['category']
            context['filter'] = filter
            context['slug'] = slug
        return context




class ListPostsBySearch(ListView):

    context_object_name = 'posts'
    template_name = 'civilopedia/index.html'
    paginate_by = 4
    allow_empty = True

    def get_queryset(self):
        search = self.request.GET.get('s')
        queryset = Post.objects.filter(Q(name_post__icontains=search) | Q(content__icontains=search), is_published=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('s')
        s = f's={search}&'
        count_posts = len(self.get_queryset())
        result = f'{f"Все статьи по запросу {repr(search)}" if count_posts != 0 else f"По запросу {repr(search)} ничего не найдено"}'
        context['s'] = s
        context['result'] = result
        context['count_posts'] = count_posts
        return context





class AddTags(LoginRequiredMixin, View):


    def get(self, request, *args, **kwargs):
        form = TagForm()
        return render(request, 'civilopedia/add_tags.html', context={'form': form})


    def post(self, request, *args, **kwargs):
        validate_and_add_tags(request, request.POST)
        return redirect(reverse('civilopedia:add_post'))





# AddOrChangePostMixin - класс в наших utils, который наследуется от View

class CreatePost(LoginRequiredMixin, AddOrChangePostMixin):

    def my_render(self, request,form):
        return render(request, 'civilopedia/add_post.html', context={'form': form,})


    def get(self, request, *args, **kwargs):
        form = PostForm()
        return self.my_render(request, form)


    def post(self, request, *args, **kwargs):
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # функция, которую мы наследуем от AddOrChangePostMixin, см. в utils.py
            self.add_or_change_post(request=request, form=form)

            return redirect(reverse_lazy('civilopedia:posts'))
        return self.my_render(request, form)






# AddOrChangePostMixin - класс в наших utils, который наследуется от View

class ChangePost(LoginRequiredMixin, AddOrChangePostMixin):

    def my_render(self, request, form, post):
        context = {'form': form, 'post': post,}
        return render(request, 'civilopedia/change_post.html', context=context)


    def get(self, request, slug, *args, **kwargs):
        post = Post.objects.get(slug=slug)
        form = PostForm(instance=post)
        context = {'form': form, 'post': post,}
        return self.my_render(request, form, post)


    def post(self, request, slug, *args, **kwargs):
        post = Post.objects.get(slug=slug)
        form = PostForm(data=request.POST, instance=post, files=request.FILES)
        if form.is_valid():
            # функция, которую мы наследуем от AddOrChangePostMixin, см. в utils.py
            self.add_or_change_post(request=request, form=form)

            return redirect(reverse_lazy('civilopedia:posts'))
        return self.my_render(request, form, post)




class ViewPost(DetailView):
    model = Post
    template_name = 'civilopedia/view_post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewPost, self).get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['tags'] = self.object.tags.all()
        return context




def controller(request):
    greating = 'Hello World'
    hide = ''.join([choice(printable[10:62]) for i in range(randrange(20,51))])
    context = {'greating': greating, 'hide': hide,}
    return render(request, 'civilopedia/index.html', context=context)



def index(request):
    posts = Post.objects.filter(is_published=True)
    context = {'posts': posts,}

    print(f'\n\n###########################################################\n'
          f'\n\nposts - {posts}\n\n'
          
          f'\n###########################################################\n\n')

    return render(request, 'civilopedia/index.html', context=context)






def tags_page(request):
    all_tags = Tag.objects.annotate(cnt=Count('posts', filter=F('posts__is_published'))).filter(cnt__gt=0).order_by('name_tag')
    context = {'all_tags': all_tags}


    data = []
    tags = ['а',]
    s = 'а'
    for item in all_tags:
        if item.name_tag[0] != s:
            data.append(tags)
            s = item.name_tag[0]
            tags = [s, item]
        else:
            tags.append(item)
    else:
        data.append(tags)
    context['data'] = data

    print(f'\n\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n'
          f'\n\ndata - {data}\n\n'
        f'\n\nall_tags - {all_tags}\n\n'
          f'\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n')
    with open('../../../tags.txt', 'w') as f:

        for index, item in enumerate(all_tags, 1):
            f.write(f'{index}) ' + item.name_tag + '\n')

    return render(request=request, template_name='civilopedia/tags_page.html', context=context)
    # return render(request=request, template_name='civilopedia/experiments_tags_page.html', context=context)





def json_list_published_posts(request):
    posts = Post.objects.filter(is_published=True)
    data = {
        'posts' : [
            {'post_name': p.name_post,
             'id': p.pk,
             'slug': p.slug,
             'tags': [tag.name_tag for tag in p.tags.all()],
             'created': p.created,
             }
            for p in posts
        ]
    }
    return JsonResponse(data=data)



# сделать контроллер, который импортирует токен на почту
@login_required
def get_token(request):
    have_token = request.user.profile.token
    if not have_token:
        part1 = ''.join([str(randrange(10)) for i in range(10)])
        part2 = ''.join([choice(printable[:62]) for i in range(35)])
        token = part1 + ' : ' + part2
        new_token = Token.objects.create(token=token)
        have_token = new_token.token
        have_token.save()
        return render(request, 'civilopedia/get_token.html', context={'token': new_token.token})
    return render(request, 'civilopedia/get_token.html', context={})
    # return HttpResponse(f'token:\n\n\n<h1>{token}</h1>')

