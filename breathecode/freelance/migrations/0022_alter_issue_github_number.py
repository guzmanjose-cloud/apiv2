# Generated by Django 3.2.16 on 2022-11-15 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelance', '0021_auto_20220920_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='github_number',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]