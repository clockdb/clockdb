# Generated by Django 2.2.15 on 2021-10-16 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_privatechatroom_roomchatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatechatroom',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]