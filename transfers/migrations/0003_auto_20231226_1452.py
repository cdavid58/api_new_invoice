# Generated by Django 3.2.8 on 2023-12-26 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0002_auto_20231226_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='code',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='ipo',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='price',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='quantity',
        ),
        migrations.CreateModel(
            name='Details_Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=150)),
                ('product', models.CharField(max_length=250)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('ipo', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('transfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transfers.transfer')),
            ],
        ),
    ]
