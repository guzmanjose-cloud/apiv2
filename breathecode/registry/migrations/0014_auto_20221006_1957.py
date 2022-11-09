# Generated by Django 3.2.15 on 2022-10-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0013_alter_asset_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='cleaning_status',
            field=models.CharField(
                blank=True,
                choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'), ('WARNING', 'Warning')],
                default='PENDING',
                help_text='Internal state automatically set by the system based on cleanup',
                max_length=20,
                null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='cleaning_status_details',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='last_cleaning_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='readme_raw',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]