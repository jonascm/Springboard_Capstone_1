## LAST PIECE OF CODE: fill in databases!
#phew


import os
import urllib.request
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotels1.settings')
django.setup()
from hotelfinder.models import Rating, Hotel
import pandas as pd
import datetime

# create 1k users
from django.contrib.auth.models import User
print('Creating virtual users')
for usr in range(1799):
    user = User.objects.create_user(username=str(usr), email=str(usr) + '@email.com', password='password')

# create all ratings
# create all hotels
print('Creating hotels')
df = pd.read_csv('Hotels_clean_merged.csv')
df = df.rename(index=str, columns={"class": "starcalss"})
for row in df.iterrows():
    hotel = Hotel(name=row[1].hotel_name,
                    city=row[1].city, 
                    state=row[1].state,
                    zipcode=row[1].zip,
                    star_class=row[1].starcalss,
                    price_approx=row[1].price)

    hotel.save()


dfr = pd.read_csv('generated_ratings_1_reduced.csv', header=None, names=['item_', 'rating','user'])
print('Creating ratings')
for row in dfr.iterrows():
    rating = Rating(hotel=Hotel.objects.get(name=row[1].item_),
                    user=User.objects.get(username=str(row[1].user)),
                    stay_date=datetime.date.today(),
                    rating_OVERALL = row[1].rating)
    rating.save()

#dfr = pd.read_csv('generated_ratings_1.csv')
#print('Creating ratings')
#for row in dfr.iterrows():
#    rating = Rating(hotel=Hotel.objects.get(name=row[1].hotel_name),
#                    user=User.objects.get(username=str(row[1].user_id)),
#                    stay_date=datetime.date.today(),
#                    rating_OVERALL = row[1].ratings)
#    rating.save()



     
