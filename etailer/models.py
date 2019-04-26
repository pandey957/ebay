from django.db import models
from django.contrib.auth.models import User

class Ebay(models.Model):
    title = models.CharField(max_length=200)
    user_id = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=5)
    reference = models.CharField(max_length=15)
    room = models.IntegerField(blank=True, null=True)
    no_of_bedroom = models.IntegerField(blank=True, null=True)
    no_of_bathrooms = models.IntegerField(blank=True, null=True)
    living_area = models.IntegerField(blank=True, null=True)
    land_area = models.CharField(max_length=15)
    heating = models.CharField(max_length=15)
    construction_year = models.CharField(max_length=15)
    price_negotiable = models.CharField(max_length=3)
    detail_url = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    posting_dt = models.DateField()
    commision = models.CharField(max_length=100)
    price = models.DecimalField(max_digits = 10, decimal_places=3)
    features = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    available_from = models.DateField()
    create_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('reference', )
        ordering = ['create_dt']


# Create your models here.
