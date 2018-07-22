from django.db import models
from django.contrib.auth.models import User
from tracker.choices import STATUS_CHOICES

# Create your models here.
#Используется стандартная модель пользователя

#Модель для задачи
class Task(models.Model):
    task_name = models.CharField(max_length=255) #название задачи
    project_name = models.CharField(max_length=255)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created') #автор
    executor = models.ForeignKey(User, on_delete=models.CASCADE) #исполнитель

    status = models.CharField(max_length=255, choices=STATUS_CHOICES) #статус задачи(один на выбор из трех)

    created_at = models.DateTimeField(auto_now_add=True) #время создания задачи
    updated_at = models.DateTimeField(auto_now=True) #время обновления задачи

    def __str__(self):
        return self.task_name

#модель для описания
class Description(models.Model):
    task = models.ForeignKey(Task, related_name='descriptions', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.content

#Модель для комментариев
class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE) #задание к которому привязан комментарий
    title = models.CharField(max_length=255) #заголовок комментария
    content = models.TextField() #содержание комментария
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')

    def __str__(self):
        return self.title
