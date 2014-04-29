from django.conf.urls import patterns, url

from survey import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/?$', views.survey, name='survey'),
)
