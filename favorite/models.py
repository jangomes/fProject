from django.db import models
from store.models import Product, Variation
from accounts.models import Account
# Create your models here.


class Favorite(models.Model):
    fav_id =models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fav_id

class FavItem(models.Model):
    variations = models.ManyToManyField(Variation, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.product)
