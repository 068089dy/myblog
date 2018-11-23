import django

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


from app_blog.models import Article, Visitor, Tag, Classification
from rest_framework import mixins, generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import FactorySerializer
from .decotator import wrap_permission
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def get_token(request):
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})


from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ArticleListView(
    generics.ListAPIView,
    mixins.CreateModelMixin
):
    serializer_class = FactorySerializer.get_serializer(Article, attr_exclude=('content', 'html_content'))
    queryset = Article.objects.all()
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('classification__name', 'tags__name')
    search_fields = ('title', 'content')
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kw):
        self.serializer_class = FactorySerializer.get_serializer(Article, attr_exclude=('content', 'html_content'))
        return self.list(request, *args, **kw)

    @wrap_permission(permissions.IsAdminUser)
    def post(self, request, *args, **kwargs):
        self.serializer_class = FactorySerializer.get_serializer(Article, attr_exclude=('volume', ))
        return self.create(request, *args, **kwargs)

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = Article.objects.all()
    #     tag = self.request.query_params.get('tag', None)
    #     classification = self.request.query_params.get('classification', None)
    #     if classification is not None:
    #         # 外键过滤
    #         queryset = queryset.filter(classification__name=classification)
    #     if tag is not None:
    #         # 外键过滤
    #         queryset = queryset.filter(tags__name=tag)
    #     return queryset


class ArticleViewDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Article.objects.all()
    serializer_class = FactorySerializer.get_serializer(Article)
    # authentication_classes = (authentication.BaseAuthentication, )

    def get(self, request, *args, **kwargs):
        self.permission_classes = ()
        return self.retrieve(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def delete(self, request, *args, **kwargs):
        self.permission_classes = (permissions.IsAdminUser, )
        return self.destroy(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kw):
    #     return self.create(request, *args, **kw)

# class ArticleViewSet(viewsets.ModelViewSet):
#     """
#     查看、编辑用户的界面
#     """
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = FactorySerializer.get_serializer(Tag)

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClassificationListView(generics.ListAPIView):
    queryset = Classification.objects.all()
    serializer_class = FactorySerializer.get_serializer(Classification)

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class VisitorListView(generics.ListAPIView):
#     table = Visitor.setDb_table("visit-2018-11")
#     queryset = table.objects.all()
#     serializer_class = FactorySerializer.get_serializer(table)
#     # authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(self, request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)


from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from myblog import settings


# 创建user时生成Token
@receiver(post_save, sender=django.contrib.auth.models.User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
