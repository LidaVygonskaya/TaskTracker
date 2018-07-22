from django.contrib import admin

# Register your models here.
from tracker.models import Task, Description, Comment

admin.site.register(Task)
admin.site.register(Description)
admin.site.register(Comment)