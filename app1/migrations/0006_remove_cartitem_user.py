# Generated by Django 4.2.6 on 2023-11-17 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
    ]
