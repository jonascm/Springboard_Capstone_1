from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from django.contrib.auth.models import User
from .forms import UserCreationFormWithEmail
from django.contrib.auth import login, authenticate

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'



def SignUpWithEmail(request):
    if request.method == 'POST':
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            form.save()
	    #messages.success(request, 'Account created successfully')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationFormWithEmail()
    return render(request, 'signup.html', {'form': form})


#class SignUpWithEmail(UserCreationForm):
#    form_class = UserCreationFormWithEmail
#    success_url = reverse_lazy('login')
#    template_name = 'signup.html'
