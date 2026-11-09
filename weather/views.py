from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from django.shortcuts import render

API_URL = 'https://api.open-meteo.com/v1/forecast'
PARAMS = {
    'latitude': 65.0121, 'longitude': 25.4651, 'timezone': 'Europe/Helsinki',
    'forecast_days': 7,
    'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,is_day',
    'hourly': 'temperature_2m,precipitation_probability,weather_code',
    'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max',
}

def condition(code):
    if code == 0: return ('Clear sky', '☀️')
    if code in (1, 2): return ('Partly cloudy', '🌤️')
    if code == 3: return ('Overcast', '☁️')
    if code in (45, 48): return ('Foggy', '🌫️')
    if code in (51, 53, 55, 56, 57): return ('Drizzle', '🌦️')
    if code in (61, 63, 65, 66, 67, 80, 81, 82): return ('Rainy', '🌧️')
    if code in (71, 73, 75, 77, 85, 86): return ('Snowy', '❄️')
    if code in (95, 96, 99): return ('Thunderstorm', '⛈️')
    return ('Variable weather', '🌡️')

def dashboard(request):
    context = {'city': 'Oulu', 'error': None}
    try:
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        current, daily, hourly = data['current'], data['daily'], data['hourly']
        label, icon = condition(current['weather_code'])
        context['current'] = {**current, 'description': label, 'icon': icon}
        context['updated'] = datetime.fromisoformat(current['time']).strftime('%H:%M')
        context['today'] = datetime.now(ZoneInfo('Europe/Helsinki')).strftime('%A, %d %B %Y')
        context['sunrise'] = datetime.fromisoformat(daily['sunrise'][0]).strftime('%H:%M')
        context['sunset'] = datetime.fromisoformat(daily['sunset'][0]).strftime('%H:%M')
        context['forecast'] = [
            {'day': datetime.fromisoformat(date).strftime('%a'), 'date': datetime.fromisoformat(date).strftime('%d %b'),
             'icon': condition(code)[1], 'description': condition(code)[0], 'max': round(high), 'min': round(low), 'rain': rain}
            for date, code, high, low, rain in zip(daily['time'], daily['weather_code'], daily['temperature_2m_max'], daily['temperature_2m_min'], daily['precipitation_probability_max'])
        ]
        now_hour = datetime.fromisoformat(current['time']).replace(minute=0, second=0)
        hourly_rows = []
        for time, temp, rain, code in zip(hourly['time'], hourly['temperature_2m'], hourly['precipitation_probability'], hourly['weather_code']):
            parsed = datetime.fromisoformat(time)
            if parsed >= now_hour and len(hourly_rows) < 12:
                hourly_rows.append({'time': parsed.strftime('%H:%M'), 'temp': round(temp), 'rain': rain, 'icon': condition(code)[1]})
        context['hourly'] = hourly_rows
    except (requests.RequestException, ValueError, KeyError, TypeError):
        context['error'] = 'Weather data is temporarily unavailable. Please refresh the page in a moment.'
    return render(request, 'weather/dashboard.html', context)
