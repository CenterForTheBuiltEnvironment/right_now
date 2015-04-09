# encoding: utf-8

from django.db import models
from json_field import JSONField
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea

import random
import string

def get_survey_url():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

QUESTION_TYPES = (
    ('C', 'Continuous'),
    ('D', 'Discrete'),
    ('T', 'Text'),
    ('M', 'Multiple'),
    ('S', 'Special'),
)

class Question(models.Model):
    name = models.CharField(max_length=80)
    text = models.TextField(blank=True)
    qtype = models.CharField(max_length=1, choices=QUESTION_TYPES) 
    choices = JSONField(blank=True)
    value_map = JSONField(blank=True)

    def __unicode__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    questions = models.ManyToManyField('Question')

    def __unicode__(self):
        return self.name

class Survey(models.Model):

    date_created = models.DateTimeField('Date created', auto_now_add=True)
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=5, default=get_survey_url)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    questions = models.ManyToManyField('Question', through='SurveyQuestion')
    headline_text = models.CharField(max_length=100, default="How do you feel right now?")
    default_lead_text = """Take a short survey to help researchers and building operators 
assess your indoor environment. Start by entering your workstation or room number."""
    default_welcome_text = """<div class="col-lg-6">
    <h4>Introduction</h4>
    <p>We are Ed Arens, Hui Zhang, and Fred Bauman from the Center for the Built
    Environment at University of California Berkeley. We invite you to participate
    in a study of how office workers are sensing the thermal environment in their
    buildings.</p>

    <h4>Procedures</h4>
    <p>If you agree to participate, you will be asked to take a short web-based 
    survey about your thermal sensations and comfort 2 - 3 times a day, over the
    course of about three weeks. Each survey takes one minute to complete. We will
    suggest times of day that we would like you to take the survey and you will
    have freedom to fit it into your schedule as best you can. The survey questions 
    should cause you no physical risks or discomfort.</p>

    <h4>Benefits</h4>
    <p>There is no direct benefit to you anticipated from participating in this
    study. However, the results will be used to refine the techniques by which
    buildings are operated, and to update industry standards for designing future
    buildings with greater comfort and energy efficiency. Studies such as this have
    been instrumental to recent progress in making buildings more sustainable.</p>

    <h4>Compensation</h4>
    <p>Each week we will offer $10 certificates to Peets, Starbucks, or to one or
    two restaurants the group might suggest, for all participants who have completed
    more than 10 surveys in the week.</p>
</div>

<div class="col-lg-6">
    <h4>Confidentiality</h4>
    <p>We will use your workstation number to locate you to deliver the gift cards.
    Individual survey responses or workstation number will not be discussed with or
    shown to building management. The workstation numbers and individual survey 
    results will be kept completely confidential and be analyzed only by our study
    team at UC Berkeley. Data will be stored for use in future research projects,
    but identifiers will be destroyed by the end of the study.</p>

    <h4>Risk</h4>
    <p>As with all research, there is a chance that confidentiality could be
    compromised; however, we are taking precautions to minimize this risk.</p>

    <h4>Rights</h4>
    <p>Participation in research is completely voluntary. You have the right to
    decline to participate or to withdraw at any point in this study without loss
    of benefits to which you are otherwise entitled.</p>

    <h4>Questions</h4>
    <p>If you have any questions about this research, you may call Hui Zhang at
    510-642-6918. If you have any questions about your rights as a research 
    participant in this study, please contact UC Berkeley’s Committee for the 
    Protection of Human Subjects at 510-642-7461, or email subjects@berkeley.edu.</p>
</div>"""

    lead_text = models.TextField(default=default_lead_text)
    welcome_text = models.TextField(default=default_welcome_text)
    thank_you_text = models.TextField(default="Thanks for participating!")


    def __unicode__(self):
        return self.name

class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        exclude = ['url', 'user', 'questions']
        widgets = {
            'headline_text': Textarea(attrs={'cols': 80, 'rows': 1}),
            'lead_text': Textarea(attrs={'cols': 80, 'rows': 5}),
            'welcome_text': Textarea(attrs={'cols': 80, 'rows': 20}),
            'thank_you_text': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        help_texts = {
            'name': ('Some useful help text.'),
        }

class Data(models.Model):
    datetime = models.DateTimeField('Datetime of response')
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')
    subject_id = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=9, decimal_places=2)

class Comment(models.Model):
    datetime = models.DateTimeField('Datetime of response')
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')
    subject_id = models.CharField(max_length=50)
    comment = models.TextField()

class SurveyQuestion(models.Model):
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')
    mandatory = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
 
class Multidata(models.Model):
    datetime = models.DateTimeField('Datetime of response')
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')
    subject_id = models.CharField(max_length=50)
    multivalue = models.CommaSeparatedIntegerField(max_length=51)
