import json

from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
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

def welcome(request, survey_url):
    try:
        workstation = request.session['workstation']
        return render(request, 'survey/welcome.html', {'workstation': workstation, 'survey_url': survey_url})
    except KeyError:
        return render(request, 'survey/welcome.html', {'workstation': None, 'survey_url': survey_url })

def survey(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url) 
    modules = []
    for m in survey.modules.all():
        questions = Question.objects.filter(module=m.id)
        modules.append({'name': m.name, 'questions': questions})
        
    questions_json = []
    for m in modules:
        for q in m['questions']:
            keys= ['id', 'text', 'name', 'choices', 'value_map', 'qtype']
            obj = {k: getattr(q, k) for k in keys}
            questions_json.append(obj)

    questions_json = json.dumps(questions_json)
    ctx = { 'survey': survey, 'modules': modules, 'json': questions_json }
    return render(request, 'survey/survey.html', ctx)

@require_POST
def session(request, survey_url):
    c = {}
    c.update(csrf(request))
    qd = request.POST
    request.session['workstation'] = qd['workstation']
    return HttpResponse(200)
    #return render_to_response('survey/survey.html', c)

@require_POST
def submit(request, survey_url):
    print request.content, survey_url
    return HttpResponseRedirect('/survey/thanks/')

def thanks(request):
    return render(request, 'survey/thanks.html', {'survey': survey})

def report(request, survey_url):
    return render(request, 'survey/report.html')
