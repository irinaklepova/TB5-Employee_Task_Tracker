from django.db.models import Q, Count
from rest_framework import serializers
from trackers.models import Employee, Task
from trackers.validators import (
    RelatedTaskValidator,
    StatusTaskValidator,
    NestingOfTaskValidator,
)


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""

    class Meta:
        model = Employee
        fields = ("id", "full_name", "position")


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор модели задачи"""

    class Meta:
        model = Task
        fields = "__all__"

        validators = [
            RelatedTaskValidator(field="parent_task"),
            NestingOfTaskValidator(field="parent_task"),
            StatusTaskValidator(field="status"),
        ]


class EmployeeTrackSerializer(serializers.ModelSerializer):
    """Сериализатор для занятых сотрудников:
    - запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач
    """

    active_task_count = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True)

    @staticmethod
    def get_active_task_count(obj):
        return obj.tasks.filter(is_active=True).count()

    class Meta:
        model = Employee
        fields = (
            "full_name",
            "position",
            "tasks",
            "active_task_count",
        )
        validators = [
            RelatedTaskValidator(field="parent_task"),
            NestingOfTaskValidator(field="parent_task"),
            StatusTaskValidator(field="status"),
        ]


class ImportantTasksSerializer(serializers.ModelSerializer):
    """Сериализатор выбора свободных сотрудников для важных задач:
    - запрашивает из БД задачи, не взятых в работу, но от которых зависят другие задачи, взятые в работу.
    - реализует поиск по сотрудникам, которые могут взять такие задачи (наименее загруженный
    сотрудник или сотрудник, выполняющий родительскую задачу, если ему назначено максимум на 2
    задачи больше, чем у наименее загруженного сотрудника).
    - возвращает список объектов в формате: {Важная задача, Срок, [ФИО сотрудника]}.
    """

    tasks = TaskSerializer
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ("id", "title", "time_complete", "employees")
        validators = [
            RelatedTaskValidator(field="parent_task"),
            NestingOfTaskValidator(field="parent_task"),
            StatusTaskValidator(field="status"),
        ]

    @staticmethod
    def get_employees(self):
        important_tasks = Task.objects.filter(
            Q(is_active=False) & (Q(parent_task__is_active=True) |
                                  Q(parent_task__parent_task__is_active=True) |
                                  Q(parent_task__parent_task__parent_task__is_active=True)
                                  )
        )
        imp_task_id = []
        for task in important_tasks:
            imp_task_id.append(task.id)

        employee_min_task = (
            Employee.objects.all().annotate(task_count=Count("tasks")).order_by("task_count").first()
        )
        emt_id = employee_min_task.id
        count_employee_min_task = Task.objects.filter(executor__id=emt_id).count()
        available_employees = []
        for i in imp_task_id:
            task_parent = Task.objects.get(pk=i).parent_task
            employee_task_parent = Employee.objects.filter(tasks__id=task_parent.id).first()
            if employee_task_parent is not None:
                etp_id = employee_task_parent.id
                count_employee_task_parent = Task.objects.filter(executor__id=etp_id).count()

                if count_employee_task_parent - count_employee_min_task <= 2:
                    emp = Employee.objects.filter(pk=etp_id)
                    for e in emp:
                        if e.full_name not in available_employees:
                            available_employees.append(e.full_name)
            else:

                emp = Employee.objects.filter(pk=emt_id)
                for e in emp:
                    if e.full_name not in available_employees:
                        available_employees.append(e.full_name)

        return available_employees
