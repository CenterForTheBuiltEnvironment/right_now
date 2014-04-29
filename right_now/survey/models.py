from django.db import models
from json_field import JSONField

QUESTION_TYPES = (
    ('C', 'Continuous'),
    ('D', 'Discrete'),
    ('A', 'Acceptability Scale'),
    ('T', 'Text Response'),
)

class Module(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=80)
    text = models.TextField()
    qtype = models.CharField(max_length=1, choices=QUESTION_TYPES) 
    choices = JSONField()
    module = models.ForeignKey('Module')

    def __unicode__(self):
        return self.name

class Data(models.Model):
    date_time = models.DateTimeField('Datetime of response')
    survey = models.ForeignKey('Survey')
    question = models.ForeignKey('Question')
    subject_id = models.CharField(max_length=50)
    value = models.TextField()

class Survey(models.Model):
    date_created = models.DateTimeField('Date created')
    name = models.CharField(max_length=80)
    contact = models.EmailField()
    modules = models.ManyToManyField(Module)

    def __unicode__(self):
        return self.name
