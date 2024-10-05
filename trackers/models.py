from django.db import models
from config.settings import NULLABLE
from users.models import User


class Employee(models.Model):
    """Модель сотрудника"""

    user = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE, verbose_name="Cотрудник")
    full_name = models.CharField(max_length=200, **NULLABLE, verbose_name="Фамилия, имя, отчество")
    position = models.CharField(max_length=255, **NULLABLE, verbose_name="Должность")

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Task(models.Model):
    """Модель задачи"""

    TODO_STATUS = "ToDo"
    PROGRESS_STATUS = "In Progress"
    DONE_STATUS = "Done"
    CLOSED_STATUS = "Closed"

    STATUS_CHOICES = (
        (TODO_STATUS, "К исполнению"),
        (PROGRESS_STATUS, "В процессе"),
        (DONE_STATUS, "Выполнена"),
        (CLOSED_STATUS, "Отменена"),
    )

    title = models.CharField(max_length=250, verbose_name="Наименование задачи")
    description = models.TextField(**NULLABLE, verbose_name="Описание задачи")
    executor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="tasks",
        verbose_name="Исполнитель задачи",
    )
    status = models.CharField(
        max_length=50,
        default=TODO_STATUS,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )
    time_complete = models.DateTimeField(
        **NULLABLE, verbose_name="Дата и время выполнения"
    )
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="parent",
        verbose_name="Родительская задача",
    )
    is_active = models.BooleanField(
        default=False, verbose_name="Признак активной задачи"
    )
    is_related = models.BooleanField(
        default=False, verbose_name="Признак связанной задачи"
    )

    def __str__(self):
        return (
            f"{self.title} {self.parent_task} {self.executor} "
            f"{self.time_complete} {self.status} {self.is_related} {self.is_active}"
        )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
