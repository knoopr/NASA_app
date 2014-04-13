from django.conf.urls import url
from sunburst import views

urlpatterns = [
    # Moving to ../neovi/urls.py so that index can live at site root
    # url(r'^$', views.index, name='index'),
    url(r'^asterank_json$', views.asterank_json, name='asterank_json')
]