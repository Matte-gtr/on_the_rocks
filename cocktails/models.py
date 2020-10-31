from django.db import models
from products.models import Product


class Cocktail(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False, blank=False)
    product_measure = models.CharField(max_length=50, null=False, blank=False)
    ingredient_1 = models.CharField(max_length=70, null=False, blank=False)
    ingredient_2 = models.CharField(max_length=70, blank=True)
    ingredient_3 = models.CharField(max_length=70, blank=True)
    ingredient_4 = models.CharField(max_length=70, blank=True)
    ingredient_5 = models.CharField(max_length=70, blank=True)
    ingredient_6 = models.CharField(max_length=70, blank=True)
    ingredient_7 = models.CharField(max_length=70, blank=True)
    method = models.TextField(blank=False)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name
