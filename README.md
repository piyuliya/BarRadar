# BarRadar

BarRadar - это скрипт, который позволи найти ближайшие бары к выбранному Вами местоположению.
Для работы скрипта потребуются данные о барах с сайта открытых данных Москвы.
А так же для определения координат выбранного местоположения используется Yandex geocoder API.
Библиотека Folium послужит для визуализации географических данных и информации, которая содержит координаты и местоположения. 

## Начало работы

Установите библеотеки, необходимые для работы, перечисленные в `requirements.txt`.

Для работы Yandex geocoder API, получите API ключ в [кабинете разработчика](https://developer.tech.yandex.ru/services/) и сохраните его в файле `settings.py`:

    API_KEY = "bcc59a3b-d7d5-36аe-84сb-5а178e2edbe6"

На сайте открытых данных Москвы скачаете [данные по барам](https://data.mos.ru/opendata/7710881420-bary/data/table?versionNumber=2&releaseNumber=10). Вам понадобится формат `.json`

## Как это работает

Зпаустите скрипт. Введите интересубщий Вас адрес.

![вводим адрес]( image/ввод.png)

Перейдите по сформированной ссылке.

![ссылка](image/ссылка.png)

Откроется окно браузера с результатами.

![вы здесь](image/выздесь.png)

![wepub](image/wepub.png)

