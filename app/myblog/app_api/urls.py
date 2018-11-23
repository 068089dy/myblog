from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from app_api import urls
from .views import ArticleListView, ArticleViewDetail, TagListView, ClassificationListView, get_token
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'article', ArticleViewSet)	#连接uri /users/和view userviewset

'''
api接口

article/?page=                              # 获取文章列表
article/id                                  # 获取指定文章
comment/?article_id=                        # 获取文章评论
comment/id                                  # 获取指定评论
visitor/?page=&type=&target=&date=          # 获取访客列表
link/?type=                                 # 获取链接

'''
urlpatterns = [
    # path('', include(router.urls)),
    # path('blog/', include(urls))
    path('article/', ArticleListView.as_view()),
    url(r"article/(?P<pk>\d+)/$", ArticleViewDetail.as_view()),
    path('tag/', TagListView.as_view()),
    path('class/', ClassificationListView.as_view()),
    # path('visitor/', VisitorListView.as_view()),
    path('gettoken/', get_token),
]
