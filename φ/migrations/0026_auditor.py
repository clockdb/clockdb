# Generated by Django 3.1.4 on 2021-03-10 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('φ', '0025_auto_20210309_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Auditor', models.CharField(max_length=93)),
            ],
        ),
    ]
