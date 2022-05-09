# Generated by Django 3.2.12 on 2022-05-03 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0055_alter_utmfield_utm_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automation',
            name='entered',
            field=models.PositiveIntegerField(help_text='How many contacts have entered'),
        ),
        migrations.AlterField(
            model_name='automation',
            name='exited',
            field=models.PositiveIntegerField(help_text='How many contacts have exited'),
        ),
    ]