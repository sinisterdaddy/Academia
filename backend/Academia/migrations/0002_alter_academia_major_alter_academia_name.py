# Generated by Django 5.0 on 2024-06-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academia',
            name='major',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='academia',
            name='name',
            field=models.TextField(),
        ),
    ]
