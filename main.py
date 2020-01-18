import json
import requests
from geopy import distance
import folium
from flask import Flask
import settings

with open("bars_data.json", "r", encoding="CP1251") as my_file:
    bars_data = json.load(my_file)

bar_distance = []

user_place = input("Где вы находитесь? ")


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


user_coordinates = fetch_coordinates(settings.APIKEY, user_place)

for point in bars_data:
    bars = {}
    bars['title'] = point['Name']
    bars['latitude'] = point['Latitude_WGS84']
    bars['longitude'] = point['Longitude_WGS84']
    bar_coordinates = point['Latitude_WGS84'], point['Longitude_WGS84']
    bars['distance'] = distance.distance(user_coordinates, bar_coordinates).km
    bar_distance.append(bars)


def get_min_distance(bar_distance):
    return bar_distance['distance']


sorted_bar = sorted(bar_distance, key=get_min_distance)

m = folium.Map(
    location=user_coordinates,
    zoom_start=15,
    tiles='Stamen Terrain'
)
folium.Marker(
    location=user_coordinates,
    popup='Вы здесь',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

for nearest_bars in sorted_bar[:5]:
    nearest_bars_coordinate = nearest_bars['latitude'], nearest_bars['longitude']
    folium.Marker(
        location=nearest_bars_coordinate,
        popup=nearest_bars['title'],
        icon=folium.Icon(color='green')
    ).add_to(m)

m.save('index.html')


def show_map():
    with open('index.html') as file:
        return file.read()


app = Flask(__name__)
app.add_url_rule('/', 'bars map', show_map)
app.run('0.0.0.0')
