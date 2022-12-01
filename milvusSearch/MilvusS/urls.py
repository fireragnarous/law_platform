"""MilvusS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf.urls import url

from . import views,search

urlpatterns = [
    # path('hello/', views.hello),
    # url(r'^$', admin.site.urls),
    # path('admin', ), # , for DeBUG
    # path('runoob', views.runoob),
    url(r'^admin/$', admin.site.urls),
    url(r'^runoob/$', views.runoob),
    url(r'^search-form/$', search.search_form),
    url(r'^search/$', search.search),

]
# path(route, view, kwargs=None, name=None)  URL规则字符串，用于执行匹配的URL请求，kwargs视图使用字典类型，name反向获取
# Django2. 0中可以使用 re_path() 方法来兼容 1.x 版本中的 url() 方法，一些正则表达式的规则也可以通过 re_path() 来实现
