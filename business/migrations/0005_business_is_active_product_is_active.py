# Generated by Django 4.0.3 on 2022-09-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_business_address_alter_business_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
