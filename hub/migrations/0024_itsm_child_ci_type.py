# Generated by Django 4.0 on 2022-08-20 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0023_itsm_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsm',
            name='Child_CI_type',
            field=models.CharField(help_text='Asset Affected', max_length=200, null=True, verbose_name='Child ci name'),
        ),
    ]
