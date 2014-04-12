from django.conf.urls import url
from sunburst import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^asterank_json$', views.asterank_json, name='asterank_json')
]