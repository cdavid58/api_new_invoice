# Generated by Django 3.2.8 on 2024-01-03 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0066_alter_branch_psswd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='SS4qwU1as7', max_length=10),
        ),
    ]