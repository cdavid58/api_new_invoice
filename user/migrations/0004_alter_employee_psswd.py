# Generated by Django 3.2.8 on 2023-10-04 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20231004_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='psswd',
            field=models.CharField(default='QFL7wxiWcdPW3Zsn7dgE', max_length=20),
        ),
    ]
