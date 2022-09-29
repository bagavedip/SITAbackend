# Generated by Django 4.0 on 2022-08-25 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0029_itsm_false_positives_id_itsm_first_response_time_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itsm',
            name='Reopened',
        ),
        migrations.AddField(
            model_name='itsm',
            name='false_positives',
            field=models.CharField(help_text='false_positives', max_length=200, null=True, verbose_name='false_positives'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='reopened',
            field=models.CharField(help_text='Reopened', max_length=200, null=True, verbose_name='Reopened'),
        ),
    ]
