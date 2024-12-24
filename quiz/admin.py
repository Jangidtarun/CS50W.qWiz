from django.contrib import admin
from .models import User, Question, Choice, Result, Comment, Topic, Vote, View, UserAnswer, Quiz

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Result)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Vote)
admin.site.register(View)
admin.site.register(UserAnswer)
admin.site.register(Quiz)