from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import home, show

urlpatterns = [
    path('', home),
    url(r'^show/', show),
    # url(r'^show/([0-9]*)/$', show),
    # path('list/', showlist),
]
