# Generated by Django 2.0.6 on 2018-06-14 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replicas', '0002_add_replica_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='latency',
            options={'get_latest_by': 'modified', 'ordering': ('-modified',), 'verbose_name_plural': 'latencies'},
        ),
    ]