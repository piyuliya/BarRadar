import json
import requests
from geopy import distance
import folium
from flask import Flask
import settings

NEAREST_BARS_AMOUNT = 5


def get_bars():
    with open("bars.json", "r", encoding="CP1251") as my_file:
        initial_bars = json.load(my_file)
        return initial_bars


def fetch_coordinates(api_key, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": api_key, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_distance(user_place, initial_bars):
    user_coordinates = fetch_coordinates(settings.API_KEY, user_place) 
    bars_with_distances = []
    for point in initial_bars:
        bar_coordinates = point['Latitude_WGS84'], point['Longitude_WGS84']
        distance_to_bar = distance.distance(user_coordinates, bar_coordinates).km
        bar = {
            'title': point['Name'],
            'latitude': point['Latitude_WGS84'],
            'longitude': point['Longitude_WGS84'],
            'distance': distance_to_bar,
        }
        bars_with_distances.append(bar)
    return bars_with_distances


def get_sorted(bars_with_distances):
    sorted_bars = sorted(bars_with_distances, key=get_distance)
    return sorted_bars


def create_map(user_coordinates):
    map_for_user = folium.Map(
        location=user_coordinates,
        zoom_start=17,
    )
    return map_for_user


def show_map():
    with open('index.html') as file:
        return file.read()


def create_marker(map_for_user, user_coordinates, sorted_bars):
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
    return map_for_user.save('index.html')


if __name__ == '__main__':
    user_place = input("Где вы находитесь? ")
    app = Flask(__name__)
    app.add_url_rule('/', 'bars map', show_map)
    app.run('0.0.0.0')
    show_map()
