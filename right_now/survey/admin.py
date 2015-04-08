from django.contrib import admin
from survey.models import Survey, Module, Question, SurveyQuestion
from django.forms import TextInput, Textarea
from django.db import models

admin.site.register(Module)
admin.site.register(Question)

class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion

class SurveyAdmin(admin.ModelAdmin):
    inlines = [SurveyQuestionInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols': 80})},
    }

admin.site.register(Survey, SurveyAdmin)
