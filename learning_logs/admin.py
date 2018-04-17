from django.contrib import admin
from learning_logs.models import Topic, Entry, Comment

# Register your models here.

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Comment)
