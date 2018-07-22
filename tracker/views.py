from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.models import Task, Comment
from tracker.serializers import UserSerializer, TaskSerializer, TaskUpdateSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


#Задания, порученные текущему пользователю
class MyTasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, )


    def get_queryset(self):
        qs = super(MyTasksViewSet, self).get_queryset()
        if self.request.query_params.get('id'):
            return Task.objects.filter(executor=self.request.query_params.get('id'))
        else:
            return qs


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_fields = ('task_name', 'project_name', 'author', 'executor', 'status')

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = TaskUpdateSerializer
        return serializer_class


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



