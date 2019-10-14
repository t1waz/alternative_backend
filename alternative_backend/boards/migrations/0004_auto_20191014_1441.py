# Generated by Django 2.2.6 on 2019-10-14 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20191014_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardcompany',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='boardmodel',
            name='code',
            field=models.IntegerField(unique=True),
        ),
    ]