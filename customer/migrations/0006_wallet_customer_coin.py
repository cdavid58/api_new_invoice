# Generated by Django 3.2.8 on 2023-12-29 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_wallet_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet_customer',
            name='coin',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
