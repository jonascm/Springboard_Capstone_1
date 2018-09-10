from django.contrib import admin

# Register your models here.
from hotelfinder.models import Hotel, Rating

# basic admins
#admin.site.register(Hotel)
#admin.site.register(Rating)

# Register the Admin classes using the decorator
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    pass
    list_display = ('hotel_id','name','city','state','zipcode','star_class','price_approx')

# Register the Admin classes using the decorator
@admin.register(Rating) 
class RatingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'stay_date', 'rating_OVERALL')
