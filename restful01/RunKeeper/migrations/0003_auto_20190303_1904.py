# Generated by Django 2.1 on 2019-03-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RunKeeper', '0002_session_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='avg_speed',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='total_dist',
            field=models.FloatField(null=True),
        ),
    ]