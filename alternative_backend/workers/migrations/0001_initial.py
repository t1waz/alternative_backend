# Generated by Django 2.1.15 on 2019-12-24 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('password', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('barcode', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkerWorkHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_time', models.BigIntegerField(blank=True, null=True)),
                ('finished', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_work_finished', to='events.Event')),
                ('started', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_work_started', to='events.Event')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workers.Worker')),
            ],
        ),
    ]
