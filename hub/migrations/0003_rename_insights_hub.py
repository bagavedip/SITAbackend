# Generated by Django 4.0 on 2022-07-26 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_alter_itsm_fault_neutralization_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Insights',
            new_name='Hub',
        ),
    ]
