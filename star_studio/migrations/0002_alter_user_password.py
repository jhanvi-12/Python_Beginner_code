# Generated by Django 3.2.16 on 2022-10-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_studio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
