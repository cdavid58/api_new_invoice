# Generated by Django 3.2.8 on 2023-12-18 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0039_auto_20231206_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='psswd',
            field=models.CharField(default='UlKxo7d4vb0IKmWNDRf9', max_length=20, unique=True),
        ),
    ]
