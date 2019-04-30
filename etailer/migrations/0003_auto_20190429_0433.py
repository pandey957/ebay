# Generated by Django 2.1.5 on 2019-04-29 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etailer', '0002_ebay_house_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebay',
            name='available_from',
        ),
        migrations.AddField(
            model_name='ebay',
            name='additional_cost',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='ebay',
            name='available_from_month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ebay',
            name='available_from_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ebay',
            name='deposit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
