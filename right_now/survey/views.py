import json
import datetime
import pytz
import csv
import unicodedata
from decimal import *

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST

from survey.models import Survey, Question, Data, Comment

def index(request):
    latest_survey_list = Survey.objects.order_by('-date_created')[:5]
    template = loader.get_template('survey/index.html')
    context = RequestContext(request, {
        'latest_survey_list': latest_survey_list,
    })
    return HttpResponse(template.render(context))

@ensure_csrf_cookie
def welcome(request, survey_url):
    try:
        workstation = request.session['workstation']
        return render(request, 'survey/welcome.html', {'workstation': workstation, 'survey_url': survey_url})
    except KeyError:
        return render(request, 'survey/welcome.html', {'workstation': None, 'survey_url': survey_url })

def survey(request, survey_url):
    if request.session['workstation'] is None:
        return HttpResponseRedirect('/survey/' + survey_url)
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
    request.session['workstation'] = str(request.POST['workstation'])
    return HttpResponse(200)

@require_POST
def submit(request, survey_url):
    c = {}
    c.update(csrf(request))
    workstation = request.session['workstation']
    d = json.loads(request.body)
    now = datetime.datetime.now(pytz.utc)
    for r in d:
        q = Question.objects.get(id=r['question'])
        s = Survey.objects.get(id=r['survey'])
        if 'value' in r:
            data = Data(datetime=now, survey=s, question=q, subject_id=workstation, value=Decimal(r['value']))
            data.save()
        elif 'comment' in r:
            comment = Comment(datetime=now, survey=s, question=q, subject_id=workstation, comment=r['comment'])
            comment.save()
    return HttpResponse(200)

def thanks(request, survey_url):
    return render(request, 'survey/thanks.html', {'survey': survey})

def report(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url)
    questions = []
    for m in survey.modules.all():
        questions += Question.objects.filter(module=m)

    keys = ['id', 'name', 'text', 'qtype', 'choices', 'value_map']
    questions_json = []
    for q in questions:
        questions_json.append({ k: q.__dict__.get(k) for k in keys })
    data = Data.objects.filter(survey=survey)
    data_json = []

    keys = ['question_id','value']
    for d in data:
        data_json.append({ k: float(d.__dict__.get(k)) for k in keys })
    comments = Comment.objects.filter(survey=survey)
    comments_json = []

    keys = ['question_id', 'subject_id', 'comment']
    for c in comments: 
      comments_json.append({ k: c.__dict__.get(k) for k in keys })
    ctx = { 'survey': survey, 
            'data': json.dumps(data_json), 
            'questions': json.dumps(questions_json), 
            'comments': json.dumps(comments_json) }
    return render(request, 'survey/report.html', ctx)

def render_csv(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report-%s.csv"' % survey.name
    writer = csv.writer(response)
    data = Data.objects.filter(survey=survey)
    comments = Comment.objects.filter(survey=survey)
    local_tz = pytz.timezone('US/Pacific')
    for d in data:
        now = d.datetime.replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, d.subject_id, d.question, d.question.id, d.value])
    for c in comments:
        nfkd_comment = unicodedata.normalize('NFKD', c.comment).encode('ascii', 'ignore')
        now = c.datetime.replace(tzinfo=pytz.utc).astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, c.subject_id, c.question, c.question.id, nfkd_comment])
    return response

