# Generated by Django 4.0.3 on 2022-09-16 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0009_multimedia_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multimedia',
            name='is_active',
        ),
    ]
