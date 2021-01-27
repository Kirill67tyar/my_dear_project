from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from string import printable
from random import randrange, choice
from django.urls import reverse
from django.views import View
from accounts.models import Profile
from .forms import UserRegisterForm, UserLoginForm, UserLoginFormNavbar
from django.contrib import messages
from civilopedia.models import Post, Tag
from django.db.models import Avg, Sum, Count



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            user = login(request, user)
            messages.success(request, f'Юзер {user} успешно зарегистрирован - добро пожаловать')
            return redirect(reverse('civilopedia:posts'))

        messages.error(request, 'Что-то пошло не так при регистрации')
    else:
        form = UserRegisterForm()
    return render(request=request, template_name='accounts/register.html', context={'form': form})





class UserLogin(View):
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)  # зачем здесь именно именованный аргумент передавать - я не знаю
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Авторизация прошла успешно, милости просим=)')
            return redirect(reverse('civilopedia:posts'))
        else:
            messages.error(request, 'Что-то пошло не так при авторизации')



    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        print(f'\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
              f'request.path - {request.path}'
              f'\n@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n')
        if request.path == '/accounts/login/':
            return render(request=request, template_name='accounts/login.html', context={'form': form})
        return render(request=request,
                      template_name='../templates/inc/_inc_details/_details_for_navbar/EXP_navbar_user.html',
                      context={'form': form})
        # return render(request=request, template_name='')



def user_login(request):
    if request.method == 'POST':
        form = UserLoginFormNavbar(request.POST)  # зачем здесь именно именованный аргумент передавать - я не знаю
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request=request, username=cd['username'], password=cd['password'])
            if user is None:
                return HttpResponse('Неправильный логин или пароль')
            if not user.is_active:
                return HttpResponse('Ваш аккаунт заблокирован')
            login(request, user)
            messages.success(request, 'Авторизация прошла успешно, милости просим=)')
            return redirect(reverse('civilopedia:posts'))
        else:
            messages.error(request, 'Что-то пошло не так при авторизации')

    # if request.method == 'POST':
    #     form = UserLoginForm(data=request.POST) # зачем здесь именно именованный аргумент передавать - я не знаю
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         messages.success(request, 'Авторизация прошла успешно, милости просим=)')
    #         return redirect(reverse('civilopedia:posts'))
    #     else:
    #         messages.error(request, 'Что-то пошло не так при авторизации')
    # else:
    #     form = UserLoginForm()
    #     return render(request=request, template_name='accounts/login.html', context={'form': form})




def user_logout(request):
    logout(request)
    return redirect(reverse('civilopedia:posts'))



def controller(request):
    greating = '<h1>Hello World</h1>'
    p1 = printable[:62]
    p2 = printable
    hide = ''.join([choice(p1) for i in range(50)])
    return HttpResponse(f'{greating}\n {hide}')


def get_rating(user):
    avg_all_views = Post.objects.aggregate(avg=Avg('views'))
    avg_user_views = Post.objects.filter(author=user).aggregate(avg=Avg('views'))
    point = avg_all_views['avg'] / 100
    rating_in_percentage = avg_user_views['avg'] / point
    rating = round((100 if rating_in_percentage > 100 else rating_in_percentage) / 20, 2)
    return (rating, avg_user_views)



def filter_tags(tags):
    result = set()
    tags = [(t['tags__name_tag'], t['tags__slug']) for t in tags]
    for tag in tags:
        result.add(tag)
    result = [(elem[0], elem[-1]) for elem in result if elem[0] is not None and elem[-1] is not None]
    result.sort(key=lambda x: x[0])
    return result




@login_required
def profile(request):
    user = request.user
    number_of_publications = len(Post.objects.filter(author=user, is_published=True))
    number_of_draft_publications = len(Post.objects.filter(author=user, is_published=False))
    all_views_publications = Post.objects.filter(author=user).aggregate(count=Sum('views'))
    rating, avg_user_views = get_rating(user)
    all_tags = Post.objects.values('tags__name_tag', 'tags__slug')
    tags = filter_tags(all_tags)
    context = {
        'number_of_publications': number_of_publications,
        'number_of_draft_publications': number_of_draft_publications,
        # 'rating': rating,
        'rating': 4.1,
        'avg_user_views': avg_user_views,
        'tags': tags,
        'user_name': user,
        'all_views_publications': all_views_publications['count'],
        # 'stars': 'stars'

    }
    return render(request, 'accounts/profile.html', context=context)




@login_required
def published_or_draft(request):
    if request.method == 'GET':
        user = request.user
        type_of_posts = request.path[:-1].split('/')
        type_of_posts = type_of_posts[-1]
        schrodinger_cat = True if type_of_posts == 'published' else False
        posts = Post.objects.filter(author=user, is_published=schrodinger_cat).select_related('category')
        paginator = Paginator(posts, 10)
        num_page = request.GET.get('page', 1)
        page_obj = paginator.get_page(num_page)

        context = {
            'page_obj': page_obj,
            'user': user,
            'schrodinger_cat':schrodinger_cat,
            'type_of_posts': type_of_posts,
        }

        return render(request, 'accounts/draft.html', context=context)



