# Generated by Django 4.0 on 2022-07-26 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UseCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usecase', models.CharField(help_text='Use Case', max_length=200)),
                ('ios_name', models.CharField(help_text='IOS Name', max_length=200)),
                ('description', models.CharField(help_text='Description', max_length=200)),
                ('default', models.CharField(help_text='Default', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(help_text='Rule Name', max_length=200)),
                ('description', models.CharField(help_text='Description', max_length=200)),
                ('default', models.CharField(help_text='Default', max_length=200)),
                ('usecase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='shared_stage.usecase')),
            ],
        ),
    ]
