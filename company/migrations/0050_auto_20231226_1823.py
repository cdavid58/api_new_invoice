# Generated by Django 3.2.8 on 2023-12-26 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0049_alter_branch_psswd'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='software_company',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='H7c5MVoLEg', max_length=10),
        ),
    ]
