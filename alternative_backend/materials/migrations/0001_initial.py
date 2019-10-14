# Generated by Django 2.2.6 on 2019-10-14 15:19

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
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('price', models.FloatField()),
                ('name', models.CharField(max_length=500, unique=True)),
                ('unit', models.CharField(choices=[('kg', 'kg'), ('m2', 'm2'), ('l', 'l'), ('pcs', 'pcs')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialPriceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('established', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_established', to='events.Event')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_material', to='materials.Material')),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.MaterialCategory'),
        ),
        migrations.CreateModel(
            name='BoardModelComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Material')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.BoardModel')),
            ],
        ),
    ]
