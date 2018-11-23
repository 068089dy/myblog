"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
import app_blog.urls
import app_api.urls
import app_api.views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'article', views.ArticleListView.as_view())	#连接uri /users/和view userviewset


urlpatterns = [
    # path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include(app_api.urls)),
    path('', include(app_blog.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', app_api.views.CustomAuthToken.as_view())
    # path('api-token-auth/', views.obtain_auth_token)
]
