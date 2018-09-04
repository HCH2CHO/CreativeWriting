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
from django.conf.urls import url,include
from django.contrib import admin
import blog.views as bv
from mysite import settings



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', bv.index),
    url(r'^time/$', bv.current_datetime),
    url(r'^add/$', bv.index1),
    url(r'^index2/$', bv.index2),
    url(r'^ajax/$', bv.ajax),
    url(r'^pdf/$', bv.pdf),
    url(r'^$', bv.register, name='register'),
    url(r'^register/$',bv.register,name = 'register'),
    url(r'^login/$',bv.login),
    url(r'^save/$', bv.save),
    url(r'^CreativeWriting/$',bv.CreativeWriting),
    url(r'^loginc/$',bv.loginc),
    url(r'^signupc/$',bv.signupc),
    url(r'^xietong/$', bv.xietong),
    url(r'^datadeal/$',bv.datadeal),

]
