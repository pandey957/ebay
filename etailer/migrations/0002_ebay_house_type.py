# Generated by Django 2.1.5 on 2019-04-29 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebay',
            name='house_type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]