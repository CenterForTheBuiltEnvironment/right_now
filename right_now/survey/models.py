import string
import random
from django.db import models
from json_field import JSONField

QUESTION_TYPES = (
    ('C', 'Continuous'),
    ('D', 'Discrete'),
    ('T', 'Text'),
    ('S', 'Special'),
)

class Module(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=80)
    text = models.TextField(blank=True)
    qtype = models.CharField(max_length=1, choices=QUESTION_TYPES) 
    choices = JSONField(blank=True)
    value_map = JSONField(blank=True)
    module = models.ForeignKey('Module')
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

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

class Survey(models.Model):
    
    def get_survey_url():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    date_created = models.DateTimeField('Date created', auto_now_add=True)
    name = models.CharField(max_length=80)
    contact = models.EmailField()
    modules = models.ManyToManyField(Module)
    url = models.CharField(max_length=5, default=get_survey_url())

    def __unicode__(self):
        return self.name
