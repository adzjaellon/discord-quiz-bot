# Generated by Django 3.2.5 on 2021-08-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210727_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
