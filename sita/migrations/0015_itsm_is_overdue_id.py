# Generated by Django 4.0 on 2022-08-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sita', '0014_alter_itsm_sla_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsm',
            name='is_overdue_id',
            field=models.CharField(help_text='Overdue Status', max_length=200, null=True, verbose_name='is_overdue_id'),
        ),
    ]
