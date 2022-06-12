from django.shortcuts import render
from crawling import crawling_cctv
from pathfinder import path
import json

# Create your views here.

cctv_info = crawling_cctv.getInfo()
pathCoord = path.main()
longitude = [];
latitude = [];
adress = [];
manager = [];
phonenum = []
for list in cctv_info:
    longitude.append(list['longitude'])
    latitude.append(list['latitude'])
    adress.append(list['adress'])
    manager.append(list['manager_name'])
    phonenum.append(list['phonenumber'])
j_longitude = json.dumps(longitude)
j_latitude = json.dumps(latitude)
j_pathCoord = json.dumps(pathCoord)

def index(request):
    return render(request, 'map/main.html', {'longitude': j_longitude, 'latitude': j_latitude, 'adress': adress,
                                             'manager': manager, 'phonenum': phonenum, 'pathCoord': j_pathCoord})

def setting(request):
    return render(request, 'map/setting.html')
def search(request):
    return render(request, 'map/search.html', {'adress': adress})