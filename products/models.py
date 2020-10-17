from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey("Category", null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    detail = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    size = models.CharField(max_length=12)
    proof = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
                                 blank=True, default=0.0)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    STAR_CHOICES = (
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Very Good'),
    )
    user = models.ForeignKey(User, related_name='reviews',
                             on_delete=models.RESTRICT)
    product = models.ForeignKey("Product", related_name='reviews',
                                on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(default=3, choices=STAR_CHOICES)
    review = models.TextField(null=True, blank=True)
    anon = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
