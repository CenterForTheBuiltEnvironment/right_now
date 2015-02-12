from django.contrib import admin
from survey.models import Survey, Module, Question, SurveyQuestion

admin.site.register(Module)
admin.site.register(Question)

class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion

class SurveyAdmin(admin.ModelAdmin):
    inlines = [SurveyQuestionInline]

admin.site.register(Survey, SurveyAdmin)
