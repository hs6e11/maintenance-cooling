# Generated by Django 4.2.5 on 2023-10-04 12:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coolingapp', '0006_alter_coolingforecast_design_cooling_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coolingforecast',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
