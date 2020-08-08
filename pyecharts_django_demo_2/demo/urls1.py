from django.conf.urls import url,re_path
from . import views


# Create your tests here.
urlpatterns = [
re_path(r'^index/$', views.index.as_view(), name='demo'),
re_path(r'^login/$',views.login.as_view(),name='demo'),
re_path(r'^index/Segment_Daily_1/$',views.Segment_Daily_1.as_view(),name='demo'),
re_path(r'^index/Segment_Daily_1_Data/$',views.Segment_Daily_1_Data.as_view(),name='demo'),
re_path(r'^index/Segment_Daily_1_Par/$',views.Segment_Daily_1_Par.as_view(),name='demo'),
#url(r'^add/$',views.add,name='add'),
]