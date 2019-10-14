# Generated by Django 2.2.6 on 2019-10-14 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('username', models.CharField(max_length=30, unique=True)),
                ('barcode', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'workers',
            },
        ),
        migrations.CreateModel(
            name='WorkerScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('started', models.BooleanField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('week', models.IntegerField()),
                ('day_name', models.CharField(max_length=80)),
                ('seconds', models.BigIntegerField()),
                ('worker_barcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workers.Worker')),
            ],
            options={
                'db_table': 'worker_scan',
            },
        ),
    ]
