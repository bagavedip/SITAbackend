# Generated by Django 4.0 on 2022-08-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0017_alter_itsm_itsm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsm',
            name='Itsm_id',
            field=models.CharField(help_text='ITSM Id', max_length=200, null=True, verbose_name='Itsm_id'),
        ),
    ]