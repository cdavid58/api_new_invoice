# Generated by Django 3.2.8 on 2023-10-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_history_invoice_history_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_pass',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
