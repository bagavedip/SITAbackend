# Generated by Django 4.0 on 2022-09-14 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0035_alter_assigntask_selectedincidents'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_id', models.CharField(help_text='incident_id', max_length=200, verbose_name='incident_id')),
                ('comment', models.CharField(help_text='comment', max_length=200, verbose_name='comment')),
                ('created', models.DateField(auto_now_add=True, help_text='created', null=True, verbose_name='created')),
            ],
        ),
        migrations.CreateModel(
            name='AddOeiComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(help_text='ticket_id', max_length=200, verbose_name='ticket_id')),
                ('comment', models.CharField(help_text='comment', max_length=200, verbose_name='comment')),
                ('created', models.DateField(auto_now_add=True, help_text='created', null=True, verbose_name='created')),
            ],
        ),
        migrations.RemoveField(
            model_name='assigntask',
            name='selectedIncidents',
        ),
        migrations.RemoveField(
            model_name='assigntask',
            name='userName',
        ),
        migrations.RemoveField(
            model_name='hub',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='itsm',
            name='comments',
        ),
        migrations.AddField(
            model_name='assigntask',
            name='assigned_user',
            field=models.CharField(help_text='assign_user', max_length=200, null=True, verbose_name='assign_user'),
        ),
        migrations.AddField(
            model_name='assigntask',
            name='created',
            field=models.DateField(auto_now_add=True, help_text='created', null=True, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='assigntask',
            name='incident_id',
            field=models.CharField(help_text='incident_id', max_length=200, null=True, unique=True, verbose_name='incident_id'),
        ),
        migrations.AddField(
            model_name='hub',
            name='last_updated_datetime',
            field=models.DateTimeField(help_text='last_updated_time', max_length=200, null=True, verbose_name='last_updated_time'),
        ),
        migrations.AddField(
            model_name='hub',
            name='target',
            field=models.CharField(help_text='target', max_length=200, null=True, verbose_name='target_ip'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='SOAR_ID',
            field=models.CharField(help_text='soar_id', max_length=200, null=True, verbose_name='Soar_id'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='due_by_time',
            field=models.CharField(help_text='Due_by_Time', max_length=200, null=True, verbose_name='Due_by_Time'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='group',
            field=models.CharField(help_text='group', max_length=200, null=True, verbose_name='group'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='is_first_response_overdue',
            field=models.CharField(help_text='Is_First_Response_Overdue', max_length=200, null=True, verbose_name='Is_First_Respose_Overdue'),
        ),
        migrations.AddField(
            model_name='itsm',
            name='target',
            field=models.CharField(help_text='Target', max_length=200, null=True, verbose_name='target'),
        ),
        migrations.AlterField(
            model_name='process',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='process',
            name='process',
            field=models.CharField(help_text='Process Name', max_length=50, null=True, verbose_name='process'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='assigned_to',
            field=models.IntegerField(help_text='Assigned To', null=True, verbose_name='assigned_to'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='categories',
            field=models.CharField(help_text='Categories', max_length=200, null=True, verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='category_count',
            field=models.IntegerField(help_text='Category Count', null=True, verbose_name='category_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='close_time',
            field=models.DateTimeField(help_text='Close Time', max_length=200, null=True, verbose_name='close_time'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='closing_reason_id',
            field=models.IntegerField(help_text='Closing Reason id', null=True, verbose_name='closing_reason_id'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='closing_user',
            field=models.IntegerField(help_text='Closing User', null=True, verbose_name='closing_user'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='credibility',
            field=models.IntegerField(help_text='Credibility', null=True, verbose_name='credibility'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='description',
            field=models.CharField(help_text='Description', max_length=200, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='destination_networks',
            field=models.CharField(help_text='Destination Network', max_length=200, null=True, verbose_name='destination_networks'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='device_count',
            field=models.IntegerField(help_text='Device Count', null=True, verbose_name='device_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='domain_id',
            field=models.IntegerField(help_text='Domain Id', null=True, verbose_name='domain_id'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='event_count',
            field=models.IntegerField(help_text='Event Count', null=True, verbose_name='event_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='flow_count',
            field=models.IntegerField(help_text='Flow Count', null=True, verbose_name='flow_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='follow_up',
            field=models.BooleanField(help_text='Follow Up', null=True, verbose_name='follow_up'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='inactive',
            field=models.BooleanField(help_text='Inactive', null=True, verbose_name='inactive'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='last_updated_datetime',
            field=models.DateTimeField(help_text='Last Updated Date Time', max_length=200, null=True, verbose_name='last_updated_datetime'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='local_destination_address_ids',
            field=models.CharField(help_text='Local destination address ids', max_length=200, null=True, verbose_name='local_destination_address_ids'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='local_destination_count',
            field=models.IntegerField(help_text='Local Destination Count', null=True, verbose_name='local_destination_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='log_sources',
            field=models.CharField(help_text='Log Sources', max_length=200, null=True, verbose_name='log_sources'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='magnitude',
            field=models.IntegerField(help_text='Magnitude', null=True, verbose_name='magnitude'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='offense_source',
            field=models.CharField(help_text='Offense Source', max_length=200, null=True, verbose_name='offense_source'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='offense_type',
            field=models.IntegerField(help_text='Offense Type', null=True, verbose_name='offense_type'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='policy_category_count',
            field=models.IntegerField(help_text='Policy category Count', null=True, verbose_name='policy_category_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='protected',
            field=models.BooleanField(help_text='Protected', null=True, verbose_name='protected'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='relevance',
            field=models.IntegerField(help_text='Relevance', null=True, verbose_name='relevance'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='remote_destination_count',
            field=models.IntegerField(help_text='Remote Destination Count', null=True, verbose_name='remote_destination_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='rule_name',
            field=models.CharField(help_text='Rule Name', max_length=200, null=True, verbose_name='rule_name'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='rules',
            field=models.CharField(help_text='Rules', max_length=200, null=True, verbose_name='rules'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='security_category_count',
            field=models.IntegerField(help_text='Security Category Count', null=True, verbose_name='security_category_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='seim_id',
            field=models.IntegerField(help_text='SIEM Id', verbose_name='seim_id'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='severity',
            field=models.IntegerField(help_text='Severity', null=True, verbose_name='severity'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='source_address_ids',
            field=models.CharField(help_text='Source address ids', max_length=200, null=True, verbose_name='source_address_ids'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='source_count',
            field=models.IntegerField(help_text='Source Count', null=True, verbose_name='source_count'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='source_network',
            field=models.CharField(help_text='Source Network', max_length=200, null=True, verbose_name='source_network'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='start_datetime',
            field=models.DateTimeField(help_text='Start Date Time', max_length=200, null=True, verbose_name='start_datetime'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='status',
            field=models.CharField(help_text='Status', max_length=200, null=True, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='siem',
            name='username_count',
            field=models.IntegerField(help_text='Username Count', null=True, verbose_name='username_count'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='AssignedUser',
            field=models.CharField(help_text='Assigned User', max_length=200, null=True, verbose_name='AssignedUser'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Case_id',
            field=models.CharField(help_text='Case Id', max_length=200, null=True, verbose_name='Case_id'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='ClosingTime',
            field=models.DateTimeField(help_text='Closing Time', max_length=200, null=True, verbose_name='ClosingTime'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Environment',
            field=models.CharField(help_text='Environment', max_length=200, null=True, verbose_name='Environment'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Important',
            field=models.BooleanField(help_text='Important', null=True, verbose_name='Important'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Incident',
            field=models.BooleanField(help_text='Incident', null=True, verbose_name='Incident'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Outcomes',
            field=models.CharField(help_text='Outcomes', max_length=200, null=True, verbose_name='Outcomes'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Ports',
            field=models.IntegerField(help_text='Ports', null=True, verbose_name='Ports'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Priority',
            field=models.CharField(help_text='Priority', max_length=200, null=True, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Products',
            field=models.CharField(help_text='Product', max_length=200, null=True, verbose_name='Products'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Reason',
            field=models.CharField(help_text='Reason', max_length=200, null=True, verbose_name='Reason'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='RootCause',
            field=models.CharField(help_text='Root Cause', max_length=200, null=True, verbose_name='RootCause'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='SOAR_ID',
            field=models.IntegerField(help_text='SOAR Id', null=True, verbose_name='SOAR_ID'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Sources',
            field=models.CharField(help_text='Sources', max_length=200, null=True, verbose_name='Sources'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Stage',
            field=models.CharField(help_text='Stage', max_length=200, null=True, verbose_name='Stage'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Status',
            field=models.CharField(help_text='Status', max_length=200, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Suspicious',
            field=models.BooleanField(help_text='Suspicious', null=True, verbose_name='Suspicious'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Tags',
            field=models.CharField(help_text='Tags', max_length=200, null=True, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='TicketIDs',
            field=models.CharField(help_text='Ticket Ids', max_length=200, verbose_name='TicketIDs'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Time',
            field=models.DateTimeField(help_text='Time', max_length=200, null=True, verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='soar',
            name='Title',
            field=models.CharField(help_text='Title', max_length=200, null=True, verbose_name='Title'),
        ),
    ]
