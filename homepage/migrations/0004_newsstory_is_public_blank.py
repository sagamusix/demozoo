# Generated by Django 2.1.15 on 2020-11-22 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_py3_strings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsstory',
            name='is_public',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]