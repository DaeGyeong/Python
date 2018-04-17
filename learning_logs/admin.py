from django.contrib import admin
from learning_logs.models import Topic, Entry, Comment

# Register your models here.

admin.site.register(Topic)
admin.site.register(Entry)
#추가
admin.site.register(Comment)
