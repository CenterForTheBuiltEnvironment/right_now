import json
import datetime
import pytz
import csv
import unicodedata
from decimal import *

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from survey.models import Survey, Question, Data, Comment, Module

@login_required
def index(request):
    surveys = Survey.objects.filter(user=request.user.id)
    template = loader.get_template('survey/index.html')
    context = RequestContext(request, {
        'surveys': surveys,
    })
    return HttpResponse(template.render(context))

@ensure_csrf_cookie
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/survey/login/')

@ensure_csrf_cookie
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/survey/')
    return render(request, 'survey/login.html', {})

def signup(request):
    if request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        # validate the username, email, and password

        if password1!=password2:
            messages.error(request, 'Passwords do not match.')
            return HttpResponseRedirect('/survey/signup/')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user already exists for the email address provided.')
            return HttpResponseRedirect('/survey/signup/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username not available.')
            return HttpResponseRedirect('/survey/signup/')

        user = User.objects.create_user(username, email=email, password=password2)
        user = authenticate(username=username, password=password2)
        login(request, user)
        messages.success(request, 'Signup successful! Create your first survey below.')
        return HttpResponseRedirect('/survey/')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/survey/')
    return render(request, 'survey/signup.html')

@ensure_csrf_cookie
def welcome(request, survey_url):
    try:
        workstation = request.session['workstation']
        return render(request, 'survey/welcome.html', {'workstation': workstation, 'survey_url': survey_url})
    except KeyError:
        return render(request, 'survey/welcome.html', {'workstation': None, 'survey_url': survey_url })

@login_required
def create(request):
    if request.POST:
        name = request.POST['survey-name']
        user = User.objects.get(id__exact=request.user.id)
        s = Survey(name=name, user=user)
        s.save()
        modules = Module.objects.filter(id__in=request.POST.getlist('modules'))
        for m in modules:
            s.modules.add(m)
        messages.success(request, 'New survey successfully created.')
        return HttpResponseRedirect('/survey/')
    else:
        modules = Module.objects.all()
        ctx = {'modules': modules}
        return render(request, 'survey/create.html', ctx)

def survey(request, survey_url):
    if request.session['workstation'] is None:
        return HttpResponseRedirect('/survey/' + survey_url)
    survey = get_object_or_404(Survey, url=survey_url) 
    modules = []
    for m in survey.modules.all():
        questions = Question.objects.filter(module=m.id).order_by('order')
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

@login_required
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

@login_required
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
