# Generated by Django 2.1.5 on 2019-04-29 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0017_auto_20190429_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebay',
            name='features',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]