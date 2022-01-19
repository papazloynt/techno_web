from django.contrib import admin

from app.models import Tag,Profile, LikesForQuestion, Question,LikesForAnswer, Answer

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(LikesForQuestion)
admin.site.register(Question)
admin.site.register(LikesForAnswer)
admin.site.register(Answer)
