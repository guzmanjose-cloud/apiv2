# Generated by Django 5.0.3 on 2024-04-02 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0004_option_is_deleted_alter_assessment_next'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='position',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='position',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
