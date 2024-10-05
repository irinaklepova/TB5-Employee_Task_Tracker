from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from trackers.models import Employee, Task
from users.permissions import IsStaff
from trackers.serializers import (
    EmployeeSerializer,
    TaskSerializer,
    EmployeeTrackSerializer,
    ImportantTasksSerializer,
)
from rest_framework.filters import OrderingFilter


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для модели сотрудника"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def perform_create(self, serializer):
        new_employee = serializer.save()
        new_employee.user = self.request.user
        new_employee.save()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (
                IsAuthenticated,
                IsStaff,
            )
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class TaskListAPIView(ListAPIView):
    """Generic-класс для вывода списка всех задач"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskRetrieveAPIView(RetrieveAPIView):
    """Generic-класс для просмотра задачи"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskCreateAPIView(CreateAPIView):
    """Generic-класс для создания задачи"""

    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.user = self.request.user
        new_task.save()


class TaskUpdateAPIView(UpdateAPIView):
    """Generic-класс для редактирования задачи"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDeleteAPIView(DestroyAPIView):
    """Generic-класс для удаления задачи"""

    queryset = Task.objects.all()


class EmployeeTrackAPIView(ListAPIView):
    """Generic-класс для вывода сортированного по количеству активных задач списка сотрудников и их задач"""

    serializer_class = EmployeeTrackSerializer
    queryset = Employee.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["active_task_count"]


class ImportantTasksForEmployeesAPIView(ListAPIView):
    """Generic-класс для вывода списка задач не взятых в работу, но от которых зависят другие задачи, взятые в работу.
    Выводит список свободных сотрудников для важных задач"""

    serializer_class = ImportantTasksSerializer

    def get_queryset(self, *args, **kwargs):

        return Task.objects.filter(
            Q(is_active=False)
            & (
                Q(parent_task__is_active=True)
                | Q(parent_task__parent_task__is_active=True)
                | Q(parent_task__parent_task__parent_task__is_active=True)
            )
        )
