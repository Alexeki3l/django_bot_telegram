# Generated by Django 4.0.3 on 2022-09-14 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0007_alter_multimedia_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multimedia',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
