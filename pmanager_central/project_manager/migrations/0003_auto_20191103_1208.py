# Generated by Django 2.2.5 on 2019-11-03 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_manager', '0002_auto_20191022_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_performer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_tasks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_manager.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_priority',
            field=models.PositiveIntegerField(choices=[(1, 'Low Priority'), (2, 'Medium Priority'), (3, 'High Priority')], default=1, verbose_name='Task Priority'),
        ),
    ]
