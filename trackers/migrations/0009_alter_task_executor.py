# Generated by Django 5.1.1 on 2024-10-02 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trackers", "0008_alter_task_executor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="executor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="trackers.employee",
                verbose_name="Исполнитель задачи",
            ),
        ),
    ]
