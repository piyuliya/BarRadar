import json
import requests
from geopy import distance
import folium
from flask import Flask
import settings

NEAREST_BARS_AMOUNT = 5
bars_distance = []
user_place = input("Где вы находитесь? ")

with open("bars.json", "r", encoding="CP1251") as my_file:
    initial_list_of_bars = json.load(my_file)


def fetch_coordinates(api_key, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": api_key, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(bars_distance):
    return bars_distance['distance']


def show_map():
    with open('index.html') as file:
        return file.read()


user_coordinates = fetch_coordinates(settings.API_KEY, user_place)

for point in initial_list_of_bars:
    bar = {
        'title': point['Name'],
        'latitude': point['Latitude_WGS84'],
        'longitude': point['Longitude_WGS84'],
    }
    bar_coordinates = point['Latitude_WGS84'], point['Longitude_WGS84']
    bar['distance'] = distance.distance(user_coordinates, bar_coordinates).km
    bars_distance.append(bar)

sorted_bars = sorted(bars_distance, key=get_distance)

map_for_user = folium.Map(
    location=user_coordinates,
    zoom_start=17,
)
folium.Marker(
    location=user_coordinates,
    popup='Вы здесь',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(map_for_user)

for nearest_bars in sorted_bars[:NEAREST_BARS_AMOUNT]:
    nearest_bars_coordinate = nearest_bars['latitude'], nearest_bars['longitude']
    folium.Marker(
        location=nearest_bars_coordinate,
        popup=nearest_bars['title'],
        icon=folium.Icon(color='green')
    ).add_to(map_for_user)

map_for_user.save('index.html')

app = Flask(__name__)
app.add_url_rule('/', 'bars map', show_map)
app.run('0.0.0.0')
