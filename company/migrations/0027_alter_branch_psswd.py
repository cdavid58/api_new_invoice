# Generated by Django 3.2.8 on 2023-10-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0026_alter_branch_psswd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='etyb3ArXyz', max_length=10),
        ),
    ]
