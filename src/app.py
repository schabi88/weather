import json
from flask import Flask, send_from_directory, render_template, jsonify, Response, make_response
from flask_cors import CORS, cross_origin
import requests
import pytemperature
import datetime
import time

app = Flask(__name__, static_url_path='',
            static_folder='frontend/node_modules/bootstrap',
            template_folder='frontend/node_modules/bootstrap')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/weather')
def get_current_weather():
    response = requests.get(
        'https://api.openweathermap.org//data/2.5/forecast?id=2841835&appid=b0992697654b1579af904ba8e1f5a294')
    json_response = response.json()
    print(json_response)
    time_stamp_dict = []
    temp_dict = []
    rain_dict = []
    for time_stamp in json_response['list']:
        # dict[list['dt']] = list['main']['temp']
        time_stamp_dict.append(datetime.datetime.utcfromtimestamp(time_stamp['dt']).time().hour + 2)
        temp_dict.append(round(pytemperature.k2c(time_stamp['main']['temp']), 1))
        rain_dict.append(time_stamp['rain']['3h'] if 'rain' in time_stamp else 0)
    print(time_stamp_dict)
    print(temp_dict)
    print(rain_dict)
    # return jsonify(['5', '6'])
    return jsonify(time_stamp_dict[:9], temp_dict[:9], rain_dict[:9])

@app.route('/forecast')
def get_forecast():
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/forecast?id=2841835&appid=b0992697654b1579af904ba8e1f5a294')
    print(response)
    return response.content


@app.route('/page')
def get_page():
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?id=2841835&appid=b0992697654b1579af904ba8e1f5a294')
    json_response = response.json()

    # get temp now
    temp_now = round(pytemperature.k2c(json_response['main']['temp']), 1)
    temp_now = '{temp_now} °C'.format(temp_now=temp_now)

    # get temp high
    temp_high = round(pytemperature.k2c(json_response['main']['temp_max']), 1)
    temp_high = 'MAX: {temp_high} °C'.format(temp_high=temp_high)

    # get temp low
    temp_low = round(pytemperature.k2c(json_response['main']['temp_min']), 1)
    temp_low = 'MIN: {temp_low} °C'.format(temp_low=temp_low)

    # get temp icon
    temp_icon = json_response['weather'][0]['icon']
    temp_icon = '{temp_icon}.png'.format(temp_icon=temp_icon)

    # todo: add summer winter time handling

    # get sunrise/sundown
    time_rise = datetime.datetime.utcfromtimestamp(json_response['sys']['sunrise']).time()
    sunrise = '{}:{}'.format(time_rise.hour + 2, time_rise.minute)
    time_down = datetime.datetime.utcfromtimestamp(json_response['sys']['sunset']).time()
    sundown = '{}:{}'.format(time_down.hour + 2, time_down.minute)
    suninfo = 'SUNRISE: {} | SUNDOWN: {}'.format(sunrise, sundown)

    return render_template('page.html', temp_now=temp_now,temp_high=temp_high, temp_low=temp_low, temp_icon=temp_icon,
                           suninfo=suninfo)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
