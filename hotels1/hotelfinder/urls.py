from django.urls import path
from hotelfinder import views


urlpatterns = [
    path('', views.index, name='index'),
    path('rate/', views.RatingCreate, name='rate_form'),
    path('search/', views.Search, name='search_form'),
]
