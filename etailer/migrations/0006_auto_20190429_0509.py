# Generated by Django 2.1.5 on 2019-04-29 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0005_auto_20190429_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebay',
            name='description',
            field=models.CharField(max_length=3000),
        ),
    ]
