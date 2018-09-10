from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid # Required for unique instances

# Create your models here.


class Hotel(models.Model):
    """Model representing a hotel"""

    hotel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular hotel')
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    star_class = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    price_approx = models.FloatField()
    # let's just start with these, I can add more in the future
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

from django.contrib.auth.models import User #Required to assign User as a borrower

class Rating(models.Model):
    """
    Model representing a specific rating of a hotel by a user.
    """
    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this rating")
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stay_date = models.DateField(null=True, blank=True)
    rating_OVERALL = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        """String for representing the Model object."""
        return self.hotel.name + ' - ' + str(self.rating_OVERALL)
    
