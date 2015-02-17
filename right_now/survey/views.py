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
from django.forms.models import modelform_factory, inlineformset_factory

from survey.models import Survey, SurveyQuestion, Question, Data, \
 Comment, Module, get_survey_url, SurveyForm

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
    survey = Survey.objects.get(url__exact=survey_url)
    ctx = {
        'survey': survey,
        'workstation': request.session.get('workstation'), 
    }
    return render(request, 'survey/welcome.html', ctx)

@login_required
def edit(request):
    if request.POST:
        params = json.loads(request.body)
        _id = params['id']
        name = params['name']
        active = params['active']
        survey = Survey.objects.get(id__exact=_id)
        if survey.user == request.user:
            survey.name = name
            survey.active = active
            survey.save()
            messages.success(request, 'Survey successfully updated.')
            return HttpResponse(status=200)

@login_required
def create(request):
    SurveyQuestionFormset = inlineformset_factory(Survey, SurveyQuestion, exclude=['survey', '_id'])
    if request.POST:
        survey_form = SurveyForm(request.POST)
        survey_instance = survey_form.save(commit=False)
        survey_instance.user_id = request.user.id
        survey_instance.save()

        survey_question_formset = SurveyQuestionFormset(request.POST)
        if survey_question_formset.is_valid():
            survey_question_instance = survey_question_formset.save(commit=False)
            for sqi in survey_question_instance:
                sqi.survey_id = survey_instance.id
                sqi.save()

        messages.success(request, 'New survey successfully created.')
        return HttpResponseRedirect('/survey/')

    else:
        survey_form = SurveyForm()
        survey_question_formset = SurveyQuestionFormset()
        ctx = {
            'survey_form': survey_form,
            'survey_question_formset': survey_question_formset
        }
        return render(request, 'survey/create.html', ctx)

def serialize_survey_questions(survey_questions):
    questions_json = []
    for q in survey_questions:

        keys = ['id', 'order', 'mandatory', 'question']
        qkeys = ['id', 'qtype', 'choices', 'text', 'value_map']
        obj = {k: getattr(q, k) for k in keys}
        obj['question'] = {k: getattr(obj['question'], k) for k in qkeys}
        questions_json.append(obj)

    return json.dumps(questions_json)

def survey(request, survey_url):
    if request.session['workstation'] is None:
        return HttpResponseRedirect('/survey/' + survey_url)
    survey = get_object_or_404(Survey, url=survey_url) 
    survey_questions = SurveyQuestion.objects.filter(survey_id=survey.id) \
                       .order_by('order').select_related('question')

    questions_json = serialize_survey_questions(survey_questions)
    ctx = { 
        'survey': survey, 
        'questions': survey_questions,
        'json': questions_json
    }
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
            data = Data(datetime=now, survey=s, question=q, 
                        subject_id=workstation, value=Decimal(r['value']))
            data.save()
        elif 'comment' in r:
            comment = Comment(datetime=now, survey=s, question=q, 
                              subject_id=workstation, comment=r['comment'])
            comment.save()
    return HttpResponse(200)

def thanks(request, survey_url):
    return render(request, 'survey/thanks.html', {'survey': survey})

@login_required
def report(request, survey_url):
    survey = get_object_or_404(Survey, url=survey_url)
    survey_questions = SurveyQuestion.objects.filter(survey_id=survey.id) \
                       .order_by('order').select_related('question')

    questions_json = serialize_survey_questions(survey_questions)

    # Numerical data
    data = Data.objects.filter(survey=survey)
    data_json = []
    keys = ['question_id','value']
    for d in data:
        data_json.append({ k: float(d.__dict__.get(k)) for k in keys })

    # Comments
    comments = Comment.objects.filter(survey=survey)
    comments_json = []
    keys = ['question_id', 'comment']
    for c in comments: 
      comments_json.append({ k: c.__dict__.get(k) for k in keys })

    ctx = { 'survey': survey, 
            'data': json.dumps(data_json), 
            'questions': questions_json, 
            'comments': json.dumps(comments_json)
    }
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
