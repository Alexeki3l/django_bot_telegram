# Generated by Django 4.0.3 on 2022-09-09 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='categorias_tienda', to='business.businesstype'),
        ),
    ]
