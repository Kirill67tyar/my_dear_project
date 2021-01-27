from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from .utils import StandardResultsSetPagination
from .serializers import PostSerializer
from civilopedia.models import Post, Tag, Category
from django.shortcuts import get_object_or_404, HttpResponse, render




# class Labor(ListModelMixin):
#     pass

# class ListPostsApi(APIView):
#
#     def get(self, request):
#         posts = Post.objects.filter(is_published=True)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)


class ListPostsAPI(ListAPIView):

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)




# class ListPostsByTagOrCategory(APIView):
#
#     def get(self, request, category=None, tag=None):
#         if category:
#             posts = Post.objects.filter(category__slug=category, is_published=True)
#         elif tag:
#             posts = Post.objects.filter(tag__slug=tag)
#         pass



class ViewPostAPI(RetrieveAPIView):

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)


# Когда будешь писать сериалайзеры для просмотра и изменения черновика, открой страницу 381 django_book
# там подробно написано про авторизацию и ограничение доступа
# В конроллер наследуемый от APIView добавь аттрибут:
# authentcation_class = (BasicAuthentication,)
# permission_classes = (IsAuthenticated,)

