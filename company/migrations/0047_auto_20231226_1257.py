# Generated by Django 3.2.8 on 2023-12-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0046_alter_branch_psswd'),
    ]

    operations = [
        migrations.AddField(
            model_name='consecutive',
            name='tras',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='X0NuYnl3yp', max_length=10),
        ),
    ]