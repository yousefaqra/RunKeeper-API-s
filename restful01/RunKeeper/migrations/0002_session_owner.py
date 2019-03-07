# Generated by Django 2.1 on 2019-03-01 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RunKeeper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Session', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
