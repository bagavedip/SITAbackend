# Generated by Django 4.0 on 2022-08-18 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0012_remove_assets_assettype_alter_assets_criticality'),
    ]

    operations = [
        migrations.AddField(
            model_name='itsm',
            name='sla_id',
            field=models.IntegerField(help_text='sla_id', null=True, verbose_name='sla_id'),
        ),
    ]
