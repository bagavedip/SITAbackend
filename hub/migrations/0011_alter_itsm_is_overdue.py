# Generated by Django 4.0 on 2022-08-17 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0010_itsm_is_overdue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsm',
            name='is_overdue',
            field=models.CharField(help_text='Overdue Status', max_length=200, null=True, verbose_name='is_overdue'),
        ),
    ]
