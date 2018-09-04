"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import blog.views as bv

urlpatterns = [
    url(r'^$', bv.CreativeWriting),
    url(r'^CreativeWriting/$',bv.CreativeWriting),

    url(r'^index/', bv.index),
    url(r'^loginc/$', bv.loginc),
    url(r'^signupc/$', bv.signupc),
    url(r'^xietong/$', bv.xietong),
    url(r'^datadeal/$', bv.datadeal),
    url(r'^ajax/$', bv.ajax),
    url(r'^save/$', bv.save),
    #电影推荐
    url(r'^update/$',bv.update),
    url(r'^get_info/$', bv.get_info),
    url(r'^get_movie/$',bv.get_movie),
    url(r'^KGRS2/$',bv.KGRS2),

]
