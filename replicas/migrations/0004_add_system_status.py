# Generated by Django 2.0.6 on 2018-08-23 01:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('replicas', '0003_update_latency_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemStatus',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('replica', models.OneToOneField(help_text='the replica running on this system', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='status', serialize=False, to='replicas.Replica')),
                ('hostname', models.CharField(blank=True, help_text='hostname identified by OS', max_length=255, null=True)),
                ('os', models.CharField(blank=True, help_text='operating system name, e.g. darwin, linux', max_length=255, null=True)),
                ('platform', models.CharField(blank=True, help_text='specific os version e.g. ubuntu, linuxmint', max_length=255, null=True)),
                ('platform_version', models.CharField(blank=True, help_text='operating system version number', max_length=255, null=True)),
                ('active_procs', models.IntegerField(blank=True, help_text='number of active processes', null=True)),
                ('uptime', models.BigIntegerField(blank=True, help_text='number of seconds the host has been online', null=True)),
                ('total_ram', models.BigIntegerField(blank=True, help_text='total amount of RAM on the system', null=True)),
                ('available_ram', models.BigIntegerField(blank=True, help_text='RAM available for programs to allocate (from kernel)', null=True)),
                ('used_ram', models.BigIntegerField(blank=True, help_text='amount of RAM used by programs (from kernel)', null=True)),
                ('used_ram_percent', models.FloatField(blank=True, help_text='percentage of RAM used by programs', null=True)),
                ('filesystem', models.CharField(blank=True, help_text='the type of filesystem at root', max_length=255, null=True)),
                ('total_disk', models.BigIntegerField(blank=True, help_text='total amount of disk space available at root directory', null=True)),
                ('free_disk', models.BigIntegerField(blank=True, help_text='total amount of unused disk space at root directory', null=True)),
                ('used_disk', models.BigIntegerField(blank=True, help_text='total amount of disk space used by root directory', null=True)),
                ('used_disk_percent', models.FloatField(blank=True, help_text='percentage of disk space used by root directory', null=True)),
                ('cpu_model', models.CharField(blank=True, help_text='the model of CPU on the machine', max_length=255, null=True)),
                ('cpu_cores', models.IntegerField(blank=True, help_text='the number of CPU cores detected', null=True)),
                ('cpu_percent', models.FloatField(blank=True, help_text='the percentage of all cores being used over the last 5 seconds', null=True)),
                ('go_version', models.CharField(blank=True, help_text='the version of Go for the currently running instance', max_length=255, null=True)),
                ('go_platform', models.CharField(blank=True, help_text='the platform compiled for the currently running instance', max_length=255, null=True)),
                ('go_architecture', models.CharField(blank=True, help_text='the chip architecture compiled for the currently running instance', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'system status',
                'verbose_name_plural': 'system statuses',
                'db_table': 'system_statuses',
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
            },
        ),
    ]