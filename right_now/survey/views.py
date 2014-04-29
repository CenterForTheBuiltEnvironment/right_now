from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST

from survey.models import Survey, Question

def index(request):
    latest_survey_list = Survey.objects.order_by('-date_created')[:5]
    template = loader.get_template('survey/index.html')
    context = RequestContext(request, {
        'latest_survey_list': latest_survey_list,
    })
    return HttpResponse(template.render(context))

def survey(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url) 
    modules = []
    for m in survey.modules.all():
        questions = Question.objects.filter(module=m.id)
        modules.append({'name': m.name, 'questions': questions})
    ctx = {'survey': survey, 'modules': modules}
    return render(request, 'survey/survey.html', ctx)

@require_POST
def submit(request, survey_url):
    print request.content, survey_url
    return HttpResponseRedirect('/survey/thanks/')

def thanks(request):
    return render(request, 'survey/thanks.html', {'survey': survey})

def report(request, survey_url):
    return render(request, 'survey/report.html')
