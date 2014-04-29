from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from survey.models import Survey

def index(request):
    latest_survey_list = Survey.objects.order_by('-date_created')[:5]
    template = loader.get_template('survey/index.html')
    context = RequestContext(request, {
        'latest_survey_list': latest_survey_list,
    })
    return HttpResponse(template.render(context))

def survey(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url)
    return render(request, 'survey/survey.html', {'survey': survey})
