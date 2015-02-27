from django.conf.urls import patterns, url

from survey import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^questions/$', views.questions, name='questions'),

    url(r'^create/$', views.create, name='create'),
    url(r'^create/(?P<survey_id>\d+)/$', views.create, name='create'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/?$', views.welcome, name='welcome'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/survey\/?$', views.survey, name='survey'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/session\/?$', views.session, name='session'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/submit\/?$', views.submit, name='submit'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/report\/?$', views.report, name='report'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/csv\/?$', views.render_csv, name='render_csv'),
    url(r'^(?P<survey_url>([A-Z]|[0-9]){5})\/thanks\/?$', views.thanks, name='thanks'),
)
