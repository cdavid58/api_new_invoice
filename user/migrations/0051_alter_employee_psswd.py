# Generated by Django 3.2.8 on 2023-12-28 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0050_alter_employee_psswd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='psswd',
            field=models.CharField(default='wz5pqm4LKVxJP9w7tzv9', max_length=20, unique=True),
        ),
    ]
