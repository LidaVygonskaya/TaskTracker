from django.contrib.auth.models import User
from rest_framework import serializers

from tracker.models import Task, Description, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name',)


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ('content',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = ('task','title', 'content', 'author')



class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('executor', 'status')


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    descriptions = DescriptionSerializer(many=True)
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Task
        fields = ('id', 'task_name', 'project_name', 'author', 'executor', 'status', 'descriptions', 'comments')

    def create(self, validated_data):
        description_data = validated_data.pop('descriptions')
        task = Task.objects.create(**validated_data)
        Description.objects.create(task=task, **(description_data.pop()))
        return task
    #
    # def partial_update(self, instance, validated_data):
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.executor = validated_data.get('executor', instance.executor)
    #     instance.save()
    #     return instance
