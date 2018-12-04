from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import home, show, Note, Blog, BlogFeed, Link, About, Tag, Search

urlpatterns = [
    path('', home),
    url(r'^show/', show),
    url(r'^search/', Search.as_view()),
    url(r'^note/', Note.as_view()),
    url(r'^blog/', Blog.as_view()),
    url(r'^link/', Link.as_view()),
    url(r'^tag/', Tag.as_view()),
    url(r'^about/', About.as_view()),
    url(r'^rss/', BlogFeed()),

    # url(r'^show/([0-9]*)/$', show),
    # path('list/', showlist),
]
