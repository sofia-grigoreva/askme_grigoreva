from django.contrib import admin
from app import models
from django.contrib.auth.models import User

admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Profile)
admin.site.register(models.Tag)
admin.site.register(models.QuestionLike)
admin.site.register(models.AnswerLike)