# Generated by Django 3.1.4 on 2021-03-09 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('φ', '0023_cashflow_repaymentsofconvertible'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashflow',
            name='IssuanceOfConvertible',
            field=models.IntegerField(default=0),
        ),
    ]
