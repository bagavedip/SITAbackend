# Generated by Django 4.0 on 2022-09-14 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0036_addcomment_addoeicomment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itsm',
            name='Description',
            field=models.CharField(help_text='Description', max_length=2000, null=True, verbose_name='Description'),
        ),
    ]