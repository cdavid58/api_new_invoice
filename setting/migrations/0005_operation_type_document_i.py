# Generated by Django 3.2.8 on 2023-10-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0004_payment_form_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_api', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type_Document_I',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
            ],
        ),
    ]
