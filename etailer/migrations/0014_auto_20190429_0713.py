# Generated by Django 2.1.5 on 2019-04-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0013_auto_20190429_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebay',
            name='address',
            field=models.CharField(max_length=200),
        ),
    ]
