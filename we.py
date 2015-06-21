#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import conf
import requests
import argparse


def color(component, val):
    if component == "temperature":
        if conf.imperial:
            val_unit = float(val) * 1.8 + 32.
        else:
            val_unit = float(val)
        if int(val) in conf.temp_color:
            col = conf.temp_color[int(val)]
        else:
            col = 196
    elif component == "wind":
        if conf.imperial:
            val_unit = float(val) / 1.609
        else:
            val_unit = float(val)
        if int(val) in conf.wind_color:
            col = conf.wind_color[int(val)]
        else:
            col = 196
    return ("\033[38;5;{0}m{1:.0f}\033[0m".format(col, val_unit))


def format_temp(temperature, feels_like):
    if feels_like < temperature:
        return ("{0:<18} - {1:<18}{2:<8}".format(color("temperature",
                feels_like), color("temperature", temperature),
                conf.unit_temp[conf.imperial]))
    else:
        return ("{0:<18} - {1:<18}{2:<8}".format(color("temperature",
                temperature), color("temperature", feels_like),
                conf.unit_temp[conf.imperial]))


def format_wind(windspeed, winddir):
    return ("{0} {1:<30}".format(conf.wind_direction[winddir], color("wind",
            windspeed) + conf.unit_wind[conf.imperial]))


def format_visibility(visibility):
    if conf.imperial:
        visibility = float(visibility) * 0.621
    else:
        visibility = float(visibility)
    return ("{0:.2f}{1:<13}".format(visibility, conf.unit_vis[conf.imperial]))


def format_rain(rainfall):
    if conf.imperial:
        rainfall = float(rainfall) * 0.039
    else:
        rainfall = float(rainfall)
    return ("{0:.2f} {1}".format(rainfall, conf.unit_rain[conf.imperial]))


def format_condition(condition):
    ret = []
    icon = []
    if condition['weatherCode'] in conf.codes:
        icon = conf.codes[condition['weatherCode']]
    else:
        icon = conf.icon['unknown']
    ret.append("{0}{1:<17}".format(icon[0], str(condition['weatherDesc'][0]['value'])[:17]))
    ret.append("{0}{1}".format(icon[1], format_temp(condition['tempC'], condition['FeelsLikeC'])))
    ret.append("{0}{1}".format(icon[2], format_wind(condition['windspeedKmph'], condition['winddir16Point'])))
    ret.append("{0}{1}".format(icon[3], format_visibility(condition['visibility'])))
    ret.append("{0}{1}".format(icon[4], format_rain(condition['precipMM'])))
    return ret


def print_day_header(weather, date):
    t = time.strptime(str(date), "%Y-%m-%d")
    date_format = time.strftime("%a %-d %B", t)
    date_adjustment = int(len(date_format) / 2)

    top_left = (62 - (date_adjustment + 2))
    top_right = len(date_format) + 4
    mid_left = (30 - (date_adjustment + 2))
    mid_right = ((23 - date_adjustment) + 4 - len(date_format) % 2)
    bottom_left = 16 - (date_adjustment + 2)
    bottom_mid_left = date_adjustment + 1
    bottom_mid_right = ((date_adjustment + 2) + len(date_format) % 2)
    bottom_right = (((4 - date_adjustment) + 4) - len(date_format) % 2)

    sunrise = "\033[38;5;220m{0}\033[0m".format(weather['astronomy'][0]['sunrise'])
    sunset = "\033[38;5;026m{0}\033[0m".format(weather['astronomy'][0]['sunset'])
    print(" " * top_left + "┌" + "─" * top_right + "┐\n"
          "                               ┌" + "─" * mid_left + "┤  " +
          date_format + "  ├" + "─" * mid_right + "┐\n"
          "            High               │           Low" + " " *
          bottom_left + "└" + "─" * bottom_mid_left + "┬" +
          "─" * bottom_mid_right + "┘" + " " * bottom_right +
          "Sunrise            │            Sunset             \n"
          "┌──────────────────────────────┼──────────────────────────────┼────"
          "──────────────────────────┼──────────────────────────────┐"
    )
    print("│            {0:<33}│            {1:<33}│           {2:<34}│           {3:<34}│".format(
        color("temperature", weather['maxtempC']), color("temperature", weather['mintempC']),
        sunrise, sunset)
    )


def print_day(weather):
    print(
        "├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤\n"
        "│           Morning            │            Midday            │           Evening            │            Night             │\n"
        "├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤"
    )
    for row in range(0,4):
        print("│{0}│{1}│{2}│{3}│".format(
              format_condition(weather['morning'])[row],
              format_condition(weather['midday'])[row],
              format_condition(weather['evening'])[row],
              format_condition(weather['night'])[row]
              ))
    print("└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘")


def get_weather(uri, key, num_days, location):
    formatted_weather = {}
    formatted_weather['days'] = {}
    parameters = {
        'key': key,
        'num_of_days': num_days,
        'q': location,
        'format': 'json'
    }
    try:
        r = requests.get(uri, params=parameters)
    except requests.exceptions.ConnectionError as err:
        print(err)
    weather_data = r.json()['data']
    formatted_weather['location'] = weather_data['request'][0]['query']
    formatted_weather['current_condition'] = weather_data['current_condition'][0]
    for day in weather_data['weather']:
        formatted_weather['days'][day['date']] = {}
        formatted_weather['days'][day['date']]['astronomy'] = day['astronomy']
        formatted_weather['days'][day['date']]['maxtempC'] = day['maxtempC']
        formatted_weather['days'][day['date']]['mintempC'] = day['mintempC']
        for hourly in day['hourly']:
            if int(hourly['time']) >= 600 and int(hourly['time']) <= 900:
                formatted_weather['days'][day['date']]['morning'] = hourly
            elif int(hourly['time']) >= 1100 and int(hourly['time']) <= 1400:
                formatted_weather['days'][day['date']]['midday'] = hourly
            elif int(hourly['time']) >= 1800 and int(hourly['time']) <= 2100:
                formatted_weather['days'][day['date']]['evening'] = hourly
            elif int(hourly['time']) >= 0 and int(hourly['time']) <= 300:
                formatted_weather['days'][day['date']]['night'] = hourly
    return formatted_weather


def get_cli_args():
    parser = argparse.ArgumentParser(description='Get the weather and display it in a terminal')
    parser.add_argument('-d', '--days', metavar='num_days', help='Specify the number of days you want included in the forecast')
    parser.add_argument('-l', '--location', help='Location for the weather report, overrides location found in conf file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_cli_args()
    if len(conf.APIKey) == 0:
        print("No API key specified, go get one from www.worldweatheronline.com and drop it in the conf file")
    uri = conf.uri
    APIKey = conf.APIKey
    num_days = conf.num_days
    if args.days:
        num_days = args.days
    location = conf.location
    if args.location:
        location = args.location
    curWeather = get_weather(uri, APIKey, num_days, location)
    curConditions = curWeather['current_condition']
    curConditions['tempC'] = curConditions['temp_C']
    print("Weather for {}".format(curWeather['location']))
    for row in range(len(format_condition(curConditions))):
        print(format_condition(curConditions)[row])
    for day in curWeather['days']:
        print_day_header(curWeather['days'][day], day)
        print_day(curWeather['days'][day])
