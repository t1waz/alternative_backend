# Generated by Django 2.2.6 on 2019-10-14 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20190922_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardmodel',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
