from django.shortcuts import render
from django.views.generic import ListView, DetailView
from Shop_app.models import Product
# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'Shop_app/home.html'

class ProdustDetails(DetailView):
    model = Product
    template_name = 'Shop_app/details_page.html'