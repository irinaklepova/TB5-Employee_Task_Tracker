from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from trackers.models import Employee, Task
from users.models import User
from django.contrib.auth.models import Group


class EmployeeTestCase(APITestCase):
    """Тесты для модели сотрудника"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test Testov", position="Test", user=self.user
        )
        self.task = Task.objects.create(
            title="Test",
            description="test",
            executor=self.employee,
            status="ToDo",
            is_active="False",
            is_related="False",
        )
        self.client.force_authenticate(user=self.user)

    def test_employee_retrieve(self):
        """Тест вывода одного сотрудника"""
        url = reverse("trackers:employees-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["full_name"], self.employee.full_name)
        self.assertEqual(data["position"], self.employee.position)

    def test_employee_create(self):
        """Тест создания сотрудника"""
        url = reverse("trackers:employees-list")
        data = {
            "full_name": "Test full_name 2",
            "position": "Test position 2",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_update(self):
        """Тест изменения пользователя"""
        url = reverse("trackers:employees-detail", args=(self.employee.pk,))
        data = {"full_name": "Test full_name NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("full_name"), "Test full_name NEW")

    def test_employee_delete(self):
        """Тест удаления пользователя"""
        url = reverse("trackers:employees-detail", args=(self.employee.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_list(self):
        """Тест вывода списка сотрудников"""
        url = reverse("trackers:employees-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "full_name": self.employee.full_name,
                "position": self.employee.position,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class EmployeeModeratorTestCase(APITestCase):
    """Тесты для модели сотрудника с пользователем модератор"""

    def setUp(self):
        self.user = User.objects.create(email="moderator@test.ru", is_staff=True)
        self.my_group = Group.objects.create(name="moderator")
        self.user.groups.add(self.my_group)
        self.user2 = User.objects.create(email="test@test.ru")
        self.user3 = User.objects.create(email="test1@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test Testov", position="Moderator", user=self.user
        )
        self.employee2 = Employee.objects.create(
            full_name="Test Testov2", position="Test2", user=self.user2
        )
        self.task = Task.objects.create(
            title="Test",
            description="test",
            executor=None,
            status="ToDo",
            is_active="False",
            is_related="False",
        )
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user2)
        self.client.force_authenticate(user=self.user3)

    def test_employee_retrieve(self):
        """Тест вывода одного сотрудника модератором"""
        url = reverse("trackers:employees-detail", args=(self.employee2.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["full_name"], self.employee2.full_name)
        self.assertEqual(data["position"], self.employee2.position)

    def test_employee_create(self):
        """Тест создания сотрудника модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("trackers:employees-list")
        data = {
            "full_name": "Test full_name 3",
            "position": "Test position 3",
            "user": self.user3,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.all().count(), 3)

    def test_employee_update(self):
        """Тест изменения сотрудника модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("trackers:employees-detail", args=(self.employee2.pk,))
        data = {"full_name": "Test full_name NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("full_name"), "Test full_name NEW")

    def test_employee_delete(self):
        """Тест удаления пользователя модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("trackers:employees-detail", args=(self.employee2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_list(self):
        """Тест вывода списка сотрудников модератором"""
        url = reverse("trackers:employees-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "full_name": self.employee.full_name,
                "position": self.employee.position,
            },
            {
                "full_name": self.employee2.full_name,
                "position": self.employee2.position,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class TaskTestCase(APITestCase):
    """Тесты для модели задачи"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test Testov", position="Test", user=self.user
        )
        self.task = Task.objects.create(
            id=1,
            title="test",
            description="test",
            status="In Progress",
            time_complete="2024-10-05T12:00:00Z",
            is_active=False,
            is_related=False,
            executor=None,
            parent_task=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        """Тест вывода одной задачи"""
        url = reverse("trackers:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.task.title)
        self.assertEqual(data["description"], self.task.description)

    def test_task_list(self):
        """Тест вывода списка задач"""
        url = reverse("trackers:task_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.task.pk,
                "title": self.task.title,
                "description": self.task.description,
                "status": self.task.status,
                "time_complete": self.task.time_complete,
                "is_active": False,
                "is_related": False,
                "executor": None,
                "parent_task": self.task.parent_task,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_task_create(self):
        """Тест создания задачи"""
        url = reverse("trackers:task_create")
        data = {
            "title": "Test NEW 2",
            "description": "test2",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_task_update(self):
        """Тест изменения задачи"""
        url = reverse("trackers:task_update", args=(self.task.pk,))
        data = {"title": "Test title NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data.get("title"), None)

    def test_task_delete(self):
        """Тест удаления задачи модератором"""
        url = reverse("trackers:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.all().count(), 1)


class TaskModeratorTestCase(APITestCase):
    """Тесты для модели задачи для модератора"""

    def setUp(self):
        self.user = User.objects.create(email="moderator@test.ru", is_staff=True)
        self.my_group = Group.objects.create(name="moderator")
        self.user.groups.add(self.my_group)
        self.employee = Employee.objects.create(
            full_name="Test Testov", position="Moderator", user=self.user
        )
        self.task = Task.objects.create(
            id=1,
            title="test",
            description="test",
            status="In Progress",
            time_complete="2024-10-05T12:00:00Z",
            is_active=False,
            is_related=False,
            executor=None,
            parent_task=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_task_create(self):
        """Тест создания задачи модератором"""
        url = reverse("trackers:task_create")
        data = {
            "title": "Test NEW 2",
            "description": "test2",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_update(self):
        """Тест изменения задачи модератором"""
        url = reverse("trackers:task_update", args=(self.task.pk,))
        data = {"title": "Test title NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Test title NEW")

    def test_task_delete(self):
        """Тест удаления задачи модератором"""
        url = reverse("trackers:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_related_task_validator(self):
        """Тест валидации связанности задачи"""
        url = reverse("trackers:task_create")
        data = {
            "title": "Test NEW 2",
            "description": "test2",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": False,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Связанная задача должна иметь родительскую"],
        )

    def test_status_task_validator(self):
        """Тест валидации статуса задачи"""
        url = reverse("trackers:task_create")
        data = {
            "title": "Test NEW 2",
            "description": "test2",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": True,
            "is_related": True,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Активная задача должна иметь статус In Progress"],
        )
