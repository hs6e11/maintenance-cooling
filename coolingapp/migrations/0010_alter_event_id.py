# Generated by Django 4.2.5 on 2023-10-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coolingapp', '0009_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
