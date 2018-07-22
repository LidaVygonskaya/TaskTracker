from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json

from tracker.models import Task

# Create your tests here.
from tracker.serializers import TaskSerializer
from django.contrib.auth.models import User


# GET METHODS
# get all tasks by URL
class GetAllTasksTest(TestCase):
    client = Client()
    user_author = 0
    user_executor = 0
    task_list = []

    def setUp(self):
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')
        self.task_list = [
            Task.objects.create(task_name="Протри полы", project_name='Работа по дому', author=self.user_author,
                                executor=self.user_executor, status="1"),
            Task.objects.create(task_name="Покушай", project_name='Готовка', author=self.user_executor,
                                executor=self.user_author, status="2"),
            Task.objects.create(task_name="Протри пыль", project_name='Работа по дому', author=self.user_author,
                                executor=self.user_executor, status="3")
        ]

    def test_get_all_tasks(self):
        # Ответ API
        response = self.client.get('/api/v1/tasks/')

        # Ответ базы данных
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user_author.delete()
        self.user_executor.delete()
        for task in self.task_list:
            task.delete()


# get one task by its id
class GetOneTaskTest(TestCase):
    client = Client()
    task_id = 0
    user_author = 0
    user_executor = 0
    task = 0

    def setUp(self):
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')
        self.task = Task.objects.create(task_name="Протри полы", project_name='Работа по дому', author=self.user_author,
                                   executor=self.user_executor, status="1")
        self.task_id = self.task.id

    def test_get_one_task(self):
        # Ответ API
        response = self.client.get('/api/v1/tasks/' + str(self.task_id) + '/')

        # Ответ базы данных
        task = Task.objects.get(id=self.task_id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user_executor.delete()
        self.user_author.delete()
        self.task.delete()


# class for filtered tasks
class GetFilteredTasks(TestCase):
    client = Client()
    user_id = 0
    user_author = 0
    user_executor = 0
    task_list = []

    def setUp(self):
        Task.objects.all().delete()
        User.objects.all().delete()
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')

        self.user_id = self.user_author.id
        self.task_list = [
            Task.objects.create(task_name="Протри полы", project_name='Работа по дому', author=self.user_author,
                                executor=self.user_executor, status="1"),
            Task.objects.create(task_name="Покушай", project_name='Готовка', author=self.user_executor,
                                executor=self.user_author,
                                status="2"),
            Task.objects.create(task_name="Протри пыль", project_name='Работа по дому', author=self.user_author,
                                executor=self.user_executor, status="3"),
            Task.objects.create(task_name="Протри пыль", project_name='Работа по дому', author=self.user_author,
                                executor=self.user_executor, status="1")]

    def test_get_task_with_same_status(self):
        # Ответ API
        response = self.client.get('/api/v1/tasks/' + '?status=1')
        # Ответ базы данных
        tasks = Task.objects.filter(status="1")

        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_with_same_name(self):
        response = self.client.get('/api/v1/tasks/' + '?task_name=Протри+пыль')

        tasks = Task.objects.filter(task_name='Протри пыль')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_with_same_author(self):
        response = self.client.get('/api/v1/tasks/' + '?author=' + str(self.user_id))

        tasks = Task.objects.filter(author=User.objects.get(id=self.user_id))
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_with_same_project_name(self):
        response = self.client.get('/api/v1/tasks/' + '?project_name=Работа+по+дому')

        tasks = Task.objects.filter(project_name='Работа по дому')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user_author.delete()
        self.user_executor.delete()
        for task in self.task_list:
            task.delete()


# POST запросы
class CreateNewTask(TestCase):
    client = Client()
    valid_payload = {}
    invalid_payload = {}
    user_author = 0
    user_executor = 0

    def setUp(self):
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')

        self.valid_payload = {
            "task_name": "Поиграй в компьютер",
            "project_name": "Развлечения",
            "executor": self.user_executor.id,
            "status": "1",
            "descriptions": [{"content": "Не играй в жестокие игры"}]
        }

        self.invalid_payload = {
            "task_name": "",
            "project_name": "Развлечения",
            "executor": "dfsgdfg",
            "status": "5",
            "descriptions": []
        }

    def test_create_valid_task(self):
        self.client.force_login(self.user_author)
        response = self.client.post('/api/v1/tasks/', data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_task(self):
        response = self.client.post('/api/v1/tasks/', data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.user_author.delete()
        self.user_executor.delete()


class CreateNewComment(TestCase):
    client = Client()
    task = 0
    user_author = 0
    user_executor = 0
    task_id = 0

    def setUp(self):
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')
        self.task = Task.objects.create(task_name="Протри полы", project_name='Работа по дому', author=self.user_author,
                                   executor=self.user_executor, status="1")
        self.task_id = self.task.id

        self.valid_payload = {
            "task": self.task_id,
            "title": "Готовность",
            "content": "Как выдумаете задание уже выполнено?"
        }

        self.invalid_payload = {
            "task": "",
            "title": "Готовность",
            "content": "Как выдумаете задание уже выполнено?"
        }

    def test_create_valid_comment(self):
        self.client.force_login(self.user_author)
        response = self.client.post('/api/v1/comments/', data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_task(self):
        self.client.force_login(self.user_author)
        response = self.client.post('/api/v1/comments/', data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.user_author.delete()
        self.user_executor.delete()
        self.task.delete()


# DELETE запрос
class DeleteSingleTask(TestCase):
    task_id = 0
    task = 0
    user_executor = 0
    user_author = 0
    client = Client()

    def setUp(self):
        self.user_author = User.objects.create(username='ivan', first_name='ivan', last_name='ivanov')
        self.user_executor = User.objects.create(username='fedor', first_name='fedor', last_name='fedorov')
        self.task = Task.objects.create(task_name="Протри полы", project_name='Работа по дому', author=self.user_author,
                                   executor=self.user_executor, status="1")
        self.task_id = self.task.id

    def test_valid_delete_task(self):
        response = self.client.delete('/api/v1/tasks/' + str(self.task_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_task(self):
        response = self.client.delete('/api/v1/tasks/' + str(self.task_id + 1) + '/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        self.task.delete()
        self.user_executor.delete()
        self.user_author.delete()
