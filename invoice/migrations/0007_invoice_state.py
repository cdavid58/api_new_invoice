# Generated by Django 3.2.8 on 2023-10-26 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_invoice_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='state',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]