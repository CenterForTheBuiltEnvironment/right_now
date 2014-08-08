from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'right_now.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^survey/', include('survey.urls')), 
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='survey/', permanent=False))
)
