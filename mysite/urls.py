from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
import CRSapp.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('CRSapp.urls')),
                       #url(r'^db', CRSapp.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^CRSapp/', include('CRSapp.urls')),
)

urlpatterns += staticfiles_urlpatterns()