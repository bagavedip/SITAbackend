# Generated by Django 4.0 on 2022-08-19 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sita', '0018_alter_itsm_itsm_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itsm',
            old_name='sla_id',
            new_name='category_id',
        ),
        migrations.RemoveField(
            model_name='itsm',
            name='is_overdue_id',
        ),
    ]
