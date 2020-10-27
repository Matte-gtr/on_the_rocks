from django.db import models
from django.contrib.auth.models import User
from products.models import Product


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
    product = models.ForeignKey(Product, related_name='reviews',
                                on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(default=3, choices=STAR_CHOICES)
    review = models.TextField(null=True, blank=True)
    anon = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
