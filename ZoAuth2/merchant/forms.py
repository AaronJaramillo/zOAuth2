from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from merchant.models import Product, Currency

PERIOD_CHOICES = [
    ('hours', 'Hours'),
    ('days', 'Days'),
    ('weeks', 'Weeks'),
    ('months', 'Months')
]

class TimePeriodSelector(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs=attrs),
            forms.Select(attrs=attrs, choices=PERIOD_CHOICES)
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        #return [value.days, value.hours, value.minutes, value.seconds]
        #pass
        return [None, None]
        #if value:
        #    return [value]

    def value_from_datadict(self, data, files, name):
        number, units = super().value_from_datadict(data, files, name)
        number = int(number)
        print(number)
        print(units)
        if units == 'days':
            obj = timedelta(days=number)
            return obj
        if units == 'hours':
            obj = timedelta(hours=number)
            print(obj)
            return obj
        if units == 'weeks':
            obj = timedelta(weeks=number)
            return obj
        if units == 'months':
            obj = timedelta(days=number*30)
            print(obj)
            return obj
        else:
            obj = timedelta(days=30)
            print(obj)
            return obj


        #integer, duration_unit = super().value_from_datadict(data, files, name)
        #return [integer, duration_unit]


class TimePeriodMultiField(forms.MultiValueField):
    #widget = TimePeriodSelector()
    def __init__(self, **kwargs):
        error_messages = {
            'incomplete': 'Enter a Time Period'
        }
        fields = (
            forms.IntegerField(),
            forms.CharField()
        )
        super().__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=True, **kwargs
        )

    def compress(self, value):
        if value[1] == 'hours':
            return datetime.timedelta(hours=value[0])
        elif value[1] == 'days':
            return datetime.timedelta(days=value[0])
        elif value[1] == 'weeks':
            return datetime.timedelta(weeks=value[0])
        elif value[1] == 'months':
            return datetime.timedelta(months=value[0])
        else:
            return None

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'address', 'period', 'scope', 'price']
        widgets = {
            'period': TimePeriodSelector()
        }
    price = forms.DecimalField()
    def clean_price(self):
        return self.cleaned_data['price'] * (10**8)
