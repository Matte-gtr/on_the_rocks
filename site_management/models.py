from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField

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
    review = models.TextField(blank=True)
    anon = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="user_profile")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=80, blank=True)
    country = CountryField(blank_label="Country",
                           null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """ creates or updates a users profile """
    if created:
        UserProfile.objects.create(user=instance)
    instance.user_profile.save()
