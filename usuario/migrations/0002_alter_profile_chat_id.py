# Generated by Django 4.0.3 on 2022-09-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]