from django.db import models

# This model won't be used for storage, but for Django's ORM compatibility
class Items(models.Model):
    class Meta:
        managed = False  # Django won't create a table for this model
        app_label = 'inventory'