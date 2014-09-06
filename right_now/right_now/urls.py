from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^survey/', include('survey.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='survey/', permanent=False))
)
