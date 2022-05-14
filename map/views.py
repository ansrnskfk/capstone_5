from django.shortcuts import render
from cctv import crawling

# Create your views here.

def index(request):
    longitude = crawling.getLng()
    latitude = crawling.getLat()
    adress = crawling.getAdress()
    manager = crawling.getManager()
    phonenum = crawling.getPhonenum()

    return render(request, 'map/main.html', {'longitude': longitude, 'latitude': latitude, 'adress': adress, 'manager': manager, 'phonenum': phonenum})

def setting(request):
    return render(request, 'map/setting.html')
def search(request):
    return render(request, 'map/search.html')