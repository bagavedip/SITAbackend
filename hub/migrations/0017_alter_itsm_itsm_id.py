# Generated by Django 4.0 on 2022-08-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0016_alter_itsm_itsm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsm',
            name='Itsm_id',
            field=models.IntegerField(help_text='ITSM Id', null=True, verbose_name='Itsm_id'),
        ),
    ]
