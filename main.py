import json

import requests
from pyg2plot import Plot
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.output import put_html

from classes.db_model import *

admin_login = False
user_login = False

config(title="PyFlora Plant Monitor", theme="dark")

img = open('images/logo2.png', 'rb').read()


# sys.setrecursionlimit(10000)

def login_form():
    global admin_login
    global user_login
    login_input = input_group("Login", [
        input('Username', name='username', value="admin"),
        input('Password', type="password", name='password', value="2241")])
    a = Login_User(login_input['username'], login_input['password'], False)
    a.login()
    if a.login_status == "admin":
        toast('Admin Login! 🔔')
        admin_login = True
        body(graf)
    elif a.login_status == "user":
        toast('Login OK! 🔔')
        user_login = True
        body(graf)
    else:
        toast('Login Failed! 🔔')
        login_form()


def logout():
    global admin_login
    global user_login
    admin_login = False
    user_login = False
    clear(scope='main')
    clear(scope='footer')
    body(login_form)


def body(body_function, *args, **kwargs):
    clear(scope='header')
    clear(scope='main')
    clear(scope='footer')
    header()
    try:
        with use_scope('main'):
            return body_function(*args, **kwargs)
    except Exception as e:
        print(e)
    finally:
        footer()


def main_buttons_callback(btn):
    if btn == 'Pots':
        body(pots)
    elif btn == 'Plants':
        body(plants)
    elif btn == 'My Profile':
        body(my_profile)
    elif btn == 'Admin Panel':
        body(admin_panel)
    elif btn == 'Logout':
        body(logout)


def plants_buttons_callback(btn, plant_id, plant_name):
    if btn == 'Delete ' + plant_name:
        print('Delete ' + plant_name)
        a = Delete_Plant(plant_id)
        a.delete_plant()
        body(plants)
    if btn == 'Edit ' + plant_name:
        print('Edit ' + plant_name)
        body(edit_plant, plant_id)


def header():
    with use_scope('header', clear=True):
        put_image(img, format="png").style("align-self: center;")
        if admin_login:
            put_buttons(['Pots', 'Plants', 'My Profile', 'Admin Panel', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")
        if user_login:
            put_buttons(['Pots', 'Plants', 'My Profile', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")


def footer():
    # remove(scope='footer')
    with use_scope('footer', clear=True):
        put_text("Made by Goran Jumić")


def admin_panel():
    put_text("admin panel content")


def pots():
    put_text("pots content")

def edit_plant(id):
    plant = session.query(Plant).filter(Plant.id == id).one_or_none()
    # img = open('images/plants/' + plant.image, 'rb').read()
    plant_input = input_group("Add or Edit Plant", [
        input('Name', name='name', value=plant.name),
        input('Description', name='description', value=plant.description),

        input('Minimum Temperature - \u00b0C', name='temp_min', value=plant.temperature_min, type=NUMBER),
        input('Maximum Temperature - \u00b0C', name='temp_max', value=plant.temperature_max, type=NUMBER),
        input('Minimum Light - lx', name='light_min', value=plant.light_min, type=NUMBER),
        input('Maximum Light - lx', name='light_max', value=plant.light_max, type=NUMBER),
        input('Minimum Humidity - %', name='hum_min', value=plant.soil_humidity_min, type=NUMBER),
        input('Maximum Humidity - %', name='hum_max', value=plant.soil_humidity_max, type=NUMBER),
        input('Minimum pH', name='ph_min', value=plant.soil_ph_min, type=FLOAT),
        input('Maximum pH', name='ph_max', value=plant.soil_ph_max, type=FLOAT),
        input('Salinity - dS/m', name='sal_min', value=plant.soil_salinity_min, type=FLOAT),
        input('Salinity - dS/m', name='sal_max', value=plant.soil_salinity_max, type=FLOAT),

    ])
    a = Update_Plant(plant.id, plant_input['name'], plant_input['description'], plant_input['temp_min'], plant_input['temp_max'], plant_input['light_min'], plant_input['light_max'], plant_input['hum_min'], plant_input['hum_max'], plant_input['ph_min'], plant_input['ph_max'], plant_input['sal_min'], plant_input['sal_max'])
    a.update_plant()
    body(plants, plant.id)

def plants(id=None):
    if id == None:
        plants = session.query(Plant).all()
    else:
        plants = session.query(Plant).filter(Plant.id == id)
    for plant in plants:
        img = open('images/plants/' + plant.image, 'rb').read()
        put_row([
            put_column([
                put_code(plant.name),
                put_code(plant.description),
            ]), None,
            put_image(img, format="png").style("align-self: center;"),
        ])
        put_row([
            put_column([
                put_row([
                    put_code('Temp min: ' + str(plant.temperature_min) + " \u00b0C"), None,
                    put_code('Temp max: ' + str(plant.temperature_max) + " \u00b0C"),

                ]),
                put_row([
                    put_code('Light min: ' + str(plant.light_min) + " lx"), None,
                    put_code('Light max: ' + str(plant.light_max) + " lx"),

                ]),
                put_row([
                    put_code('Humidity min: ' + str(plant.soil_humidity_min) + " %"), None,
                    put_code('Humidity max: ' + str(plant.soil_humidity_max) + " %"),

                ]),
                put_row([
                    put_code('pH min: ' + str(plant.soil_ph_min)), None,
                    put_code('ph max: ' + str(plant.soil_ph_max)),

                ]),
                put_row([
                    put_code('Salinity min: ' + str(plant.soil_salinity_min) + " dS/m"), None,
                    put_code('Salinity max: ' + str(plant.soil_salinity_max) + " dS/m"),

                ]),
                put_buttons(['Edit ' + plant.name, 'Delete ' + plant.name],
                            onclick=lambda btn, plant_id=plant.id, plant_name=plant.name: plants_buttons_callback(btn,
                                                                                                                  plant_id,
                                                                                                                  plant_name)).style(
                    "text-align: right; align-self: center;")
            ]), None,
        ])


def my_profile():
    put_text("my_profile content")


def graf():
    put_text("main content")
    URL_WEATHER = 'https://api.open-meteo.com/v1/forecast?latitude=45.55&longitude=18.69&hourly=temperature_2m&current_weather=true&timezone=Europe%2FBerlin&past_days=2'
    json_data = requests.get(URL_WEATHER)
    weather_data = json.loads(json_data.text)

    result = []

    for i in range(len(weather_data['hourly']['time'])):
        temp = weather_data['hourly']['temperature_2m'][i]
        time = weather_data['hourly']['time'][i]
        result.append({'time': time, 'value': temp})

    print(result)
    line = Plot("Line")

    line.set_options({
        "appendPadding": 32,
        "data": result,
        "xField": "time",
        "yField": "value",
        "label": {},
        "smooth": True,
        "lineStyle": {
            "lineWidth": 3,
        },
        "point": {
            "size": 5,
            "shape": 'diamond',
            "style": {
                "fill": "white",
                "stroke": "#5B8FF9",
                "lineWidth": 2,
            }
        }
    })

    put_html(line.render_notebook(), scope='main')


put_scope('header', content=[header()])
put_scope('main', content=[body(login_form)])
