# Generated by Django 3.2.8 on 2023-10-26 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0037_auto_20231025_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='NFjz02uDXs', max_length=10),
        ),
    ]