# Generated by Django 5.1.1 on 2024-10-01 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trackers", "0005_rename_user_task_owner_tracker"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="owner",
            new_name="user",
        ),
    ]
