# Generated by Django 3.1.4 on 2021-02-19 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('φ', '0006_cashflow_netchangeinshorttermborrowings'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditdata',
            name='TheoricalOperatingIncomeAttributableToMinorityInterests',
            field=models.FloatField(default=0),
        ),
    ]
