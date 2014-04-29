from django.conf.urls import patterns, url

from survey import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/?$', views.survey, name='survey'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/submit\/?$', views.submit, name='submit'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/report\/?$', views.report, name='report'),
    url(r'^thanks$', views.thanks, name='thanks'),
)
