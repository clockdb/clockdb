# Generated by Django 3.1.4 on 2021-03-02 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('φ', '0014_auto_20210224_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='StockPrice',
            field=models.IntegerField(default=0),
        ),
    ]
