# Generated by Django 2.2.5 on 2019-11-07 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project_manager.Project'),
        ),
        migrations.AlterField(
            model_name='team',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project_manager.Project'),
        ),
    ]
