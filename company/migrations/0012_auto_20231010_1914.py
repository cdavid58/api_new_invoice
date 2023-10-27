# Generated by Django 3.2.8 on 2023-10-11 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0005_operation_type_document_i'),
        ('company', '0011_alter_branch_psswd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='documentI',
        ),
        migrations.AddField(
            model_name='company',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setting.municipalities'),
        ),
        migrations.AddField(
            model_name='company',
            name='production',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='toke',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='type_document_identification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setting.type_document_i'),
        ),
        migrations.AddField(
            model_name='company',
            name='type_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setting.type_organization'),
        ),
        migrations.AddField(
            model_name='company',
            name='type_regime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setting.type_regimen'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='psswd',
            field=models.CharField(default='4qa6yI8DZl', max_length=10),
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_document_id', models.IntegerField()),
                ('prefix', models.CharField(max_length=7)),
                ('resolution', models.IntegerField()),
                ('resolution_date', models.CharField(max_length=10)),
                ('technical_key', models.CharField(max_length=255)),
                ('_from', models.IntegerField()),
                ('_to', models.IntegerField()),
                ('date_from', models.CharField(max_length=10)),
                ('date_to', models.CharField(max_length=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.branch')),
            ],
        ),
    ]
