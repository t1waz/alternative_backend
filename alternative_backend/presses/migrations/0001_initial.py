# Generated by Django 2.2.4 on 2019-08-24 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('press_time', models.IntegerField()),
                ('mold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_mold', to='boards.BoardModel')),
            ],
        ),
        migrations.CreateModel(
            name='MoldHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_finished', to='events.Event')),
                ('mold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_mold', to='boards.BoardModel')),
                ('press', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_press', to='presses.Press')),
                ('started', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_started', to='events.Event')),
            ],
        ),
    ]