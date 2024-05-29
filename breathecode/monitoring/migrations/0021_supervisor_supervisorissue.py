# Generated by Django 5.0.4 on 2024-04-22 06:44

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0020_alter_repositorysubscription_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_module', models.CharField(max_length=200)),
                ('task_name', models.CharField(max_length=200)),
                ('delta',
                 models.DurationField(default=datetime.timedelta(seconds=1800),
                                      help_text='How long to wait for the next execution, defaults to 30 minutes')),
                ('ran_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurrences', models.PositiveIntegerField(blank=True, default=1)),
                ('error', models.TextField(max_length=255)),
                ('ran_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='monitoring.supervisor')),
            ],
        ),
    ]