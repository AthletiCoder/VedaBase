# Generated by Django 3.0.6 on 2020-06-26 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verses', '0007_auto_20200616_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='is_leaf',
            field=models.BooleanField(default=False),
        ),
    ]