from django.contrib import admin
from survey.models import Survey, Module, Question

admin.site.register(Survey)
admin.site.register(Module)
admin.site.register(Question)

# Register your models here.
