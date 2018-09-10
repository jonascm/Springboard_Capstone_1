from django.shortcuts import render
from hotelfinder.models import Hotel, Rating

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_hotels = Hotel.objects.all().count()
    num_ratings = Rating.objects.all().count()

    
    context = {
        'num_hotels': num_hotels,
        'num_ratings': num_ratings,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from hotelfinder.forms import RateHotelModelForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def RatingCreate(request):
    #instance = RateHotelModelForm.objects.filter(user=request.user).first()
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RateHotelModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a thank you URL:
            return render(request, 'post_ratings.html')

    # If this is a GET (or any other method) create the default form.
    else:
        form = RateHotelModelForm(initial={'user': request.user})
    context = {
        'form': form,
    }
    return render(request, 'rate_form.html', context)



import os
import numpy as np
import six
from tabulate import tabulate
from surprise import Dataset
from surprise import Reader
import pandas as pd
import os
from surprise import Dataset
from surprise import Reader
from surprise import KNNBaseline


@login_required
def Search(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = SearchForm(request.POST)
        city_to_search = form.data['city']
        # I wont heck if the form is valid...
        # then I need to give that user two lists of hotels

        # 1st: train again the model

        # change this so I read from database
        # start off from the ratings:
        df = pd.DataFrame(list(Rating.objects.all().values()))
        df['user_id'] = df['user_id'].astype(str)
        reader = Reader(rating_scale=(0, 6))
        data = Dataset.load_from_df(df[['user_id', 'hotel_id', 'rating_OVERALL']], reader)

        # train kNN-Baseline on the whole collection (both, user and item-wise)
        trainset = data.build_full_trainset()

        # Build two algorithms, and train them: algo and algo_items.
        algo = KNNBaseline()
        algo.fit(trainset)
        sim_options = {'name': 'pearson_baseline', 'user_based': False}
        algo_items = KNNBaseline(sim_options=sim_options)
        algo_items.fit(trainset)

        # 2nd: top hotels for user
        # find existing hotels:



        hotels = df['hotel_id'].unique().tolist()

        user1 = request.user.username
        print(df[df['user_id'] == user1])
        print(df.info())
        print(type(user1))
        hot_ratings_user = {}
        # loop to find ratings
        for hot in hotels:
            pred = algo.predict(user1, hot)
            hot_ratings_user[hot] = pred.est
        # the whole dictionary should be done now... 
        # we need to filter hotels within the city
        df_hotels_names = pd.DataFrame(list(Hotel.objects.all().values()))
        # df_hotels_names has:  city  hotel_id  name  price_approx  star_class state  zipcode

        # this should be the first context
        sorted_hot_ratings_user = sorted(hot_ratings_user, key=hot_ratings_user.get, reverse=True)
        context1 = pd.DataFrame()
        # remove the printing part
        for key in sorted_hot_ratings_user:
             hotcurr = df_hotels_names[df_hotels_names['hotel_id']==key]
             if hotcurr['city'].to_string(index=False) == city_to_search:
                 dicttemp = pd.DataFrame({'Hotel name':[hotcurr['name'].to_string(index=False)],'Estimated rating':round(hot_ratings_user[key],2)})
                 context1 = context1.append(dicttemp, ignore_index = True)


        # 3rd: item based:
        hot_ratings_i = {}
        for hot in hotels:
            pred_i = algo_items.predict(user1, hot)
            hot_ratings_i[hot] = pred_i.est
        # the whole dictionary should be done now...
        sorted_hot_ratings_i = sorted(hot_ratings_i, key=hot_ratings_i.get, reverse=True)
        context2 = pd.DataFrame()
        for key in sorted_hot_ratings_i:
            hotcurr = df_hotels_names[df_hotels_names['hotel_id']==key]
            if hotcurr['city'].to_string(index=False) == city_to_search:
                 dicttemp = pd.DataFrame({'Hotel name':[hotcurr['name'].to_string(index=False)],'Estimated rating':round(hot_ratings_i[key],2)})
                 context2 = context2.append(dicttemp, ignore_index = True)

        # for sorting purposes, let's move it back to a df and sort it NOW...
        context1 = context1.sort_values(by='Estimated rating', ascending=False)[:10]
        context2 = context2.sort_values(by='Estimated rating', ascending=False)[:10]

        # let ma make it to the lists:
        Hotel_name_user = context1['Hotel name'].values.tolist()
        Estimated_rating_user = context1['Estimated rating'].values.tolist()
        Hotel_name_item = context2['Hotel name'].values.tolist()
        Estimated_rating_item = context2['Estimated rating'].values.tolist()

        context_rendering = {
                         'city':city_to_search,
                         'user':zip(Hotel_name_user,Estimated_rating_user),
                         'item__':zip(Hotel_name_item,Estimated_rating_item)}

        # redirect to a thank you URL:
        return render(request, 'search_results.html', context_rendering)

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchForm()
    context = {
        'form': form,
    }

    return render(request, 'search_form.html', context)



