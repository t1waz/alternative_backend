# Generated by Django 2.1.4 on 2018-12-30 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('username', models.CharField(max_length=30)),
                ('barcode', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'workers',
            },
        ),
    ]
