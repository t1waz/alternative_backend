# Generated by Django 2.1.15 on 2019-12-24 22:02

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
            name='MoldHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_mold_finished', to='events.Event')),
                ('mold', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_mold', to='boards.BoardModel')),
            ],
        ),
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('press_time', models.IntegerField()),
                ('name', models.CharField(max_length=200, unique=True)),
                ('mold', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boards.BoardModel')),
            ],
        ),
        migrations.AddField(
            model_name='moldhistory',
            name='press',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_press', to='presses.Press'),
        ),
        migrations.AddField(
            model_name='moldhistory',
            name='started',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_mold_started', to='events.Event'),
        ),
    ]
