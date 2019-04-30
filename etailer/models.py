from django.db import models
from django.contrib.auth.models import User

class Ebay(models.Model):
    title = models.CharField(max_length=200)
    user_id = models.CharField(max_length=10, blank=True, null=True)
    user_url = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=5)
    reference = models.CharField(max_length=15)
    room = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    no_of_bedroom = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    no_of_bathrooms = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    living_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    heating = models.CharField(max_length=15, blank=True, null=True)
    construction_year = models.CharField(max_length=15, blank=True, null=True)
    price_negotiable = models.CharField(max_length=3, blank=True, null=True)
    detail_url = models.CharField(max_length=300)
    address = models.CharField(max_length=200)
    posting_dt = models.DateField()
    commision = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits = 12, decimal_places=2, blank=True, null=True)
    features = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=11000, blank=True, null=True)
    available_from_year = models.IntegerField(blank=True, null=True)
    available_from_month = models.IntegerField(blank=True, null=True)
    create_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateField(auto_now=True)
    house_type = models.CharField(max_length=20, blank=True, null=True)
    additional_cost = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    user = models.CharField(max_length=150, blank=True, null=True)
    active_since = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('detail_url', )
        db_table = 'ebay'
        ordering = ['create_dt']


class HomeDay(models.Model):
    zip_code = models.CharField(max_length=5)
    state = models.CharField(max_length=100, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    additional = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    create_dt = models.DateField(auto_now_add=True)
    update_dt = models.DateField(auto_now=True)

    class Meta:
        db_table = 'homeday'
        unique_together = ('zip_code', )
