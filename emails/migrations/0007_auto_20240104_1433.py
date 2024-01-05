# Generated by Django 3.2.8 on 2024-01-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0064_alter_employee_psswd'),
        ('emails', '0006_emails_is_read_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emails',
            name='receives',
        ),
        migrations.AddField(
            model_name='emails',
            name='receives',
            field=models.ManyToManyField(to='user.Employee'),
        ),
    ]