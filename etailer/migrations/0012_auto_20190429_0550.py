# Generated by Django 2.1.5 on 2019-04-29 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0011_ebay_user_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebay',
            name='user_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
