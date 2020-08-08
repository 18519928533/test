"""HelloWorld URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,re_path
from . import views
urlpatterns = [
	re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/$', views.login,name='demo'),
    re_path(r'^dologin/$', views.dologin),
    re_path(r'^index/$', views.index,name='index'),
    re_path(r'^Daily_Segment/$', views.Daily_Segment,name='Daily_Segment'),
    re_path(r'^Daily_Segment_Data/$', views.Daily_Segment_Data),
    re_path(r'^Daily_Segment_Par/$', views.Daily_Segment_Par),
]