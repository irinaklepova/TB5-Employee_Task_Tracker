# Generated by Django 5.1.1 on 2024-10-04 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trackers", "0010_alter_task_parent_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="parent_task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="parent",
                to="trackers.task",
                verbose_name="Родительская задача",
            ),
        ),
    ]
