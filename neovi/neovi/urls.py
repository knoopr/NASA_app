from django.conf.urls import patterns, include, url
from django.contrib import admin
from sunburst import views as sbv
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neovi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', sbv.index, name='sunburst.index'),
    url(r'^sunburst/', include('sunburst.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
