# Generated by Django 3.0 on 2021-09-25 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0018_validate'),
    ]

    operations = [
        migrations.AddField(
            model_name='validate',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]