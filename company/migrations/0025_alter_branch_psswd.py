# Generated by Django 3.2.8 on 2023-10-14 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0024_alter_branch_psswd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='JzLU7Q3HCg', max_length=10),
        ),
    ]
