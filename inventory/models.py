from django.db import models
from mongoengine import Document, StringField, IntField, DecimalField

# This model won't be used for storage, but for Django's ORM compatibility
class Items(models.Model):
    class Meta:
        managed = False  # Django won't create a table for this model
        app_label = 'inventory'

class Sales(models.Model):
    period = models.CharField(max_length=10)
    product_id = models.CharField(max_length=50)
    sales_qty = models.IntegerField()
    revenue = models.FloatField()
    profit = models.FloatField()