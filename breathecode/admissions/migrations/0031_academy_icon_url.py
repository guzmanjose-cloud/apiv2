# Generated by Django 3.2.12 on 2022-02-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0030_auto_20220223_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='academy',
            name='icon_url',
            field=models.CharField(default='/static/icons/picture.png',
                                   help_text='It has to be a square',
                                   max_length=255),
        ),
    ]
