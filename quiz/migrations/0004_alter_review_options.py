# Generated by Django 3.2.5 on 2021-07-27 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-stars',)},
        ),
    ]
