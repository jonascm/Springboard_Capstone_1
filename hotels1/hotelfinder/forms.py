from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import ModelForm
from hotelfinder.models import Rating, Hotel
from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput
from django.forms.widgets import HiddenInput

class SearchForm(forms.Form):
    city = forms.ModelChoiceField(queryset=Hotel.objects.values_list('city',flat=True).distinct())





## these canbe done straight from the Models created I guess
class RateHotelModelForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user', 'hotel', 'stay_date', 'rating_OVERALL']
        widgets = {'user': forms.HiddenInput()}
