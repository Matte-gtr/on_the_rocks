from django import forms
from .models import ProductReview, UserProfile


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = [
            'stars',
            'review',
            'anon',
        ]
        labels = {
            'stars': 'Rating',
            'review': 'Review',
            'anon': 'Post as anonymous',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'postcode',
            'county',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'contact_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2 ',
            'town_or_city': 'Town or City',
            'postcode': 'Postcode',
            'county': 'County',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if not self.fields[field]:  # to be overwritten with js on clickevent
                self.fields[field].readonly = True  # to be overwritten with js on clickevent
            if field != "country":
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'user-profile-input'
            self.fields[field].label = False
