# Generated by Django 3.2.12 on 2022-03-01 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subsections', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='email',
        ),
    ]