from django.shortcuts import render, redirect, get_object_or_404
from .serializers import UserRegisterSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tourist.models import Destination
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import requests

# Create your views here.

def register(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user) 
            return redirect('login')
    else:
        serializer = UserRegisterSerializer()
    return render(request, 'registration/register.html', {'serializer': serializer})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('destination')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('destination')
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
    

def destination(request):
    if request.user.is_authenticated:
        return render(request, 'destinations/home.html')
    else:
        return redirect('login')
    
@api_view(['GET'])
def tourist(request):
    try:
        response = requests.get('https://restcountries.com/v3.1/all?fields=name')
        response.raise_for_status()
        countries = [country['name']['common'] for country in response.json()]
        return Response(sorted(countries))
    except requests.RequestException:
        countries = ['India', 'United States', 'Canada']
        return Response(countries)

@api_view(['GET'])
def get_states(request, country):
    states_data = {
        'India': ['Andhra Pradesh', 'Goa', 'Kerala', 'Odisha', 'Punjab', 'Rajasthan', 'Tamil Nadu'],
        'United States': ['Alabama', 'Alaska', 'California', 'Colorado', 'New York'],
        'Canada': ['Alberta', 'British Columbia', 'Prince Edward Island']
    }
    return Response(states_data.get(country, []))

@api_view(['GET'])
def get_districts(request, state):
    district_data = {
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli', 'Tirunelveli'],
        'Goa': ['North Goa', 'South Goa'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur'],
        'Kerala': ['Kochi', 'Kollam', 'Thrissur'],
        'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela'],
        'Punjab': ['Amritsar', 'Bathinda', 'Ludhiana'],
        'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'West Godavari'],
    }
    return Response(district_data.get(state, []))

def home(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations/home.html', {'destinations': destinations})

@login_required
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations/list.html', {'destinations': destinations})

@login_required
def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    return render(request, 'destinations/detail.html', {'destination': destination})

@login_required
def destination_create(request):
    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        weather = request.POST.get('weather')
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        google_map_link = request.POST.get('google_map_link')
        description = request.POST.get('description')
        
        destination = Destination.objects.create(
            place_name=place_name,
            weather=weather,
            country=country,
            state=state,
            district=district,
            google_map_link=google_map_link,
            description=description,
        )
        return redirect('destination_detail', id=destination.id)
    return render(request, 'destinations/create.html')

@login_required
def destination_update(request, id):
    destination = get_object_or_404(Destination, id=id)
    if request.method == 'POST':
        destination.place_name = request.POST.get('place_name')
        destination.weather = request.POST.get('weather')
        destination.country = request.POST.get('country')
        destination.state = request.POST.get('state')
        destination.district = request.POST.get('district')
        destination.google_map_link = request.POST.get('google_map_link')
        destination.description = request.POST.get('description')
        destination.save()
        return redirect('destination_detail', id=destination.id)
    return render(request, 'destinations/edit.html', {'destination': destination})

@login_required
def destination_delete(request, id):
    destination = get_object_or_404(Destination, id=id)
    destination.delete()
    return redirect('destination_list')
