import json
import os

import requests
from pyg2plot import Plot
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.output import put_html

from classes.configuration import *
from classes.db_model import *
from classes.login import *
from classes.plants import *
from classes.users import *

admin_login = False
user_login = False

config(title="PyFlora Plant Monitor", theme="dark")

img = open('images/logo2.png', 'rb').read()


def login_form():
    global admin_login
    global user_login
    global my_id
    login_input = input_group("Login", [
        input('Username', name='username', value="admin"),
        input('Password', type="password", name='password', value="2241")])
    a = Login_User(None, login_input['username'], login_input['password'], False)
    a.login()
    if a.login_status == "admin":
        toast('Admin Login! 🔔')
        admin_login = True
        my_id = a.id
        body(main_menu)
    elif a.login_status == "user":
        toast('Login OK! 🔔')
        user_login = True
        my_id = a.id
        body(main_menu)
    else:
        put_error('Login Failed! 🔔')
        login_form()


def logout():
    global admin_login
    global user_login
    global my_id
    admin_login = False
    user_login = False
    my_id = None
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
    if btn == 'Main Menu':
        body(main_menu)
    elif btn == 'Pots':
        body(pots)
    elif btn == 'Plants':
        body(plants)
    elif btn == 'My Profile':
        body(edit_user, my_id)
    elif btn == 'Admin Panel':
        body(admin_panel)
    elif btn == 'Logout':
        body(logout)


def users_buttons_callback(btn, user_id):
    if btn == 'Delete':
        print('Delete ' + str(user_id))
        if user_id == 1:
            toast('Cannot Delete Admin User! 🔔')
        else:
            a = Update_User(user_id)
            a.delete_user()
            body(admin_panel)
    elif btn == 'Edit':
        body(edit_user, user_id)
    elif btn == 'Change Password':
        body(edit_user_pass, user_id)



def plants_buttons_callback(btn, plant_id, plant_name):
    if btn == 'Delete ' + plant_name:
        print('Delete ' + plant_name)
        a = Update_Plant(plant_id)
        a.delete_plant()
        body(plants)
    elif btn == 'Edit ' + plant_name:
        print('Edit ' + plant_name)
        body(edit_plant, plant_id)
    elif btn == 'Change Picture':
        body(edit_plant_picture, plant_id, plant_name)


def header():
    with use_scope('header', clear=True):
        put_image(img, format="png").style("align-self: center;")
        if admin_login:
            put_buttons(['Main Menu', 'Pots', 'Plants', 'My Profile', 'Admin Panel', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")
        if user_login:
            put_buttons(['Main Menu', 'Pots', 'Plants', 'My Profile', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")


def footer():
    with use_scope('footer', clear=True):
        put_text("Made by Goran Jumić")


def admin_panel():
    put_html("<h2>Admin Panel</h2>")
    put_html("<b>Application Configuration</b><br><br>")
    config = session.query(Config).filter(Config.id == 1).one_or_none()
    put_table([
        ['Configuration Key', 'Configuration Value'],
        ['Location', config.city],
        ['Latitude', config.latitude],
        ['Longitude', config.longitude],
    ])
    put_button('Change', onclick=lambda: body(edit_configuration)).style("align-self: center;")

    users = session.query(User).all()
    user_list = []

    for user in users:
        user_button = put_buttons(['Edit', 'Change Password', 'Delete'],
                    onclick=lambda btn, user_id=user.id: users_buttons_callback(btn,
                                                                                user_id)).style(
            "text-align: right; align-self: center;")
        user_data = [user.username, user.first_name, user.last_name, user_button]
        user_list.append(user_data)
    put_html("<br><br><b>User Configuration</b><br><br>")
    put_table(user_list, header=['Username', 'First Name', 'Last Name', 'Actions'])
    put_button('Add User', onclick=lambda: body(edit_user)).style("align-self: center;")

def edit_configuration():
    clear(scope='header')
    config = session.query(Config).filter(Config.id == 1).one_or_none()
    config_input = input_group("Edit Application Configuration", [
        input('Location', name='city', value=config.city),
        input('Latitude', name='latitude', value=config.latitude),
        input('Longitude', name='longitude', value=config.longitude),

    ])
    a = Update_Configuration(config_input['city'], config_input['latitude'].replace(',', '.'), config_input['longitude'].replace(',', '.'))
    a.update_configuration()
    body(admin_panel)

def check_input(input):
    user = session.query(User).filter(User.username == input).one_or_none()
    if input == "":
        return 'Cannot be empty'
    elif user is not None:
        return 'Username already exists'


def edit_user(id=None):
    clear(scope='header')
    user = session.query(User).filter(User.id == id).one_or_none()
    if id == None:
        user_input = input_group("Add User", [
            input('Username', name='username', validate=check_input),
            input('Password', name='password', validate=check_input),
            input('First Name', name='first_name'),
            input('Last Name', name='last_name'),

        ])
        a = Update_User(None, user_input['username'], hashlib.md5(user_input['password'].encode('utf-8')).hexdigest(), user_input['first_name'], user_input['last_name'] )
        a.create_user()
        body(admin_panel)
    else:
        user_input = input_group("Edit User", [
            input('First Name', name='first_name', value=user.first_name),
            input('Last Name', name='last_name', value=user.last_name),

        ])
        a = Update_User(user.id, None, None, user_input['first_name'], user_input['last_name'])
        a.update_user()
        if my_id == 1:
            body(admin_panel)
        else:
            body(main_menu)

def edit_plant_picture(id, name):
    clear(scope='header')
    img = file_upload("Select a picture:", accept=".jpg", multiple=False)


    output_dir = "images/plants"
    filename = os.path.join(output_dir, name + ".jpg")
    with open(filename, 'wb') as f:
        f.write(img['content'])

    print(id)
    print(name)

def edit_user_pass(id):
    clear(scope='header')
    user = session.query(User).filter(User.id == id).one_or_none()
    user_input = input_group("Add or Edit User", [
        input('Password', name='password', validate=check_input),

    ])
    a = Update_User(user.id, None, hashlib.md5(user_input['password'].encode('utf-8')).hexdigest(), None, None)
    a.update_password()
    toast(user.username + ' new password is ' + str(user_input['password']) + ' 🔔')
    if my_id == 1:
        body(admin_panel)
    else:
        body(main_menu)


def pots():
    put_html("<h2>My Pots</h2>")


def edit_plant(id=None):
    clear(scope='header')
    plant = None

    if id is not None:
        plant = session.query(Plant).filter(Plant.id == id).one_or_none()

    plant_input = input_group("Add or Edit Plant", [
        input('Name', name='name', value=plant.name if plant else ''),
        input('Description', name='description', value=plant.description if plant else ''),

        input('Minimum Temperature - \u00b0C', name='temp_min', value=plant.temperature_min if plant else '', type=NUMBER),
        input('Maximum Temperature - \u00b0C', name='temp_max', value=plant.temperature_max if plant else '', type=NUMBER),
        input('Minimum Light - lx', name='light_min', value=plant.light_min if plant else '', type=NUMBER),
        input('Maximum Light - lx', name='light_max', value=plant.light_max if plant else '', type=NUMBER),
        input('Minimum Humidity - %', name='hum_min', value=plant.soil_humidity_min if plant else '', type=NUMBER),
        input('Maximum Humidity - %', name='hum_max', value=plant.soil_humidity_max if plant else '', type=NUMBER),
        input('Minimum pH', name='ph_min', value=plant.soil_ph_min if plant else '', type=FLOAT),
        input('Maximum pH', name='ph_max', value=plant.soil_ph_max if plant else '', type=FLOAT),
        input('Salinity - dS/m', name='sal_min', value=plant.soil_salinity_min if plant else '', type=FLOAT),
        input('Salinity - dS/m', name='sal_max', value=plant.soil_salinity_max if plant else '', type=FLOAT),

    ])
    a = Update_Plant(id, plant_input['name'], plant_input['description'], plant_input['temp_min'],
                     plant_input['temp_max'], plant_input['light_min'], plant_input['light_max'],
                     plant_input['hum_min'], plant_input['hum_max'], plant_input['ph_min'], plant_input['ph_max'],
                     plant_input['sal_min'], plant_input['sal_max'])
    if id is not None:
        a.update_plant()
        body(plants, plant.id)
    else:
        a.create_plant()
        body(plants)


def plants(id=None):
    put_html("<h1>My Plants</h1>")
    if id == None:
        plants = session.query(Plant).all()
        put_button('Add New Plant', onclick=lambda: body(edit_plant)).style("text-align: right; align-self: center;")
    else:
        plants = session.query(Plant).filter(Plant.id == id)
    for plant in plants:
        put_html("<h2>" + plant.name + " - " + plant.description + "</h2>")
        img = open('images/plants/' + plant.name + ".jpg", 'rb').read()
        put_row([
            # put_column([
            #     put_code(plant.name),
            #     put_code(plant.description),
            # ]), None,
            put_image(img, format="png").style("margin: 0 auto; display: block; margin-bottom: 20px;"),
            # put_html("<br>")
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
                put_buttons(['Edit ' + plant.name, 'Change Picture', 'Delete ' + plant.name],
                            onclick=lambda btn, plant_id=plant.id, plant_name=plant.name: plants_buttons_callback(btn,
                                                                                                                  plant_id,
                                                                                                                  plant_name)).style(
                    "text-align: right; align-self: center;")
            ]), None,
        ])


def plot_temps(latitude, longitude, location):
    put_html("<h2>Daily Forecast in " + location + "</h2>")

    URL_WEATHER = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=Europe%2FBerlin'
    json_data = requests.get(URL_WEATHER)
    weather_data = json.loads(json_data.text)

    result = []

    for i in range(len(weather_data['daily']['time'])):
        time = weather_data['daily']['time'][i]
        min_temp = weather_data['daily']['temperature_2m_min'][i]
        max_temp = weather_data['daily']['temperature_2m_max'][i]

        result.append({'time': time, 'type': 'Min', 'value': min_temp})
        result.append({'time': time, 'type': 'Max', 'value': max_temp})

    # Initialize the plot
    line = Plot("Line")
    line.set_options({
        "title": "Daily Min and Max Temperatures",
        "appendPadding": 32,
        "data": result,
        "xField": "time",
        "yField": "value",
        "seriesField": "type",  # Use 'type' field to distinguish between Min and Max temperatures
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


def main_menu():
    a = Update_Configuration()
    a.get_configuration()
    put_html("<h2>Welcome to PyFlora</h2>")
    put_html("<b>Location: " + a.city + "</b><br>").style(
        "text-align: right; align-self: center;")
    put_html("<b>Latitude: " + str(a.latitude) + "</b><br>").style(
        "text-align: right; align-self: center;")
    put_html("<b>Longitude: " + str(a.longitude) + "</b><br>").style(
        "text-align: right; align-self: center;")
    plot_temps(a.latitude, a.longitude, a.city)


put_scope('header', content=[header()])
put_scope('main', content=[body(login_form)])
