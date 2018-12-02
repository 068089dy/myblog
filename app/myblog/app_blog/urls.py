from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import home, show, note, blog, BlogFeed, link, about, tag

urlpatterns = [
    path('', home),
    url(r'^show/', show),
    url(r'^note/', note),
    url(r'^blog/', blog),
    url(r'^link/', link),
    url(r'^tag/', tag),
    url(r'^about/', about),
    url(r'^rss/', BlogFeed()),

    # url(r'^show/([0-9]*)/$', show),
    # path('list/', showlist),
]
