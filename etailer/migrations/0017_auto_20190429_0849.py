# Generated by Django 2.1.5 on 2019-04-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0016_auto_20190429_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebay',
            name='user',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
