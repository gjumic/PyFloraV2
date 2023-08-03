import json
import os
import random
from datetime import datetime, timedelta

import requests
from pyg2plot import Plot
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from pywebio.output import put_html
from sqlalchemy import desc, asc

from classes.configuration import *
from classes.db_model import *
from classes.login import *
from classes.measurements import *
from classes.plants import *
from classes.pots import *
from classes.users import *

admin_login = False
user_login = False

config(title="PyFlora Plant Monitor", theme="dark")

constant_image_dir = "images/"
constant_plants_image_dir = "images/plants/"

img = open(constant_image_dir + 'logo2.png', 'rb').read()


########################################################################################################################
# Main Screen
########################################################################################################################

def main_menu():
    global login_username

    a = Update_Configuration()
    a.get_configuration()
    put_html("<h1>Welcome to PyFlora</h1>")
    put_html("<b>User: " + login_username + "</b><br>").style(
        "text-align: right; align-self: center;")
    put_html("<b>Location: " + a.city + "</b><br>").style(
        "text-align: right; align-self: center;")
    put_html("<b>Latitude: " + str(a.latitude) + "</b><br>").style(
        "text-align: right; align-self: center;")
    put_html("<b>Longitude: " + str(a.longitude) + "</b><br>").style(
        "text-align: right; align-self: center;")
    plot_temps(a.latitude, a.longitude, a.city)


def header():
    with use_scope('header', clear=True):
        put_image(img, format="png").style("align-self: center;")
        if admin_login:
            put_buttons(['Main Screen', 'Pots', 'Plants', 'My Profile', 'Admin Panel', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")
        if user_login:
            put_buttons(['Main Screen', 'Pots', 'Plants', 'My Profile', 'Logout'],
                        onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")


def footer():
    with use_scope('footer', clear=True):
        put_text("Made by Goran Jumić")


def main_buttons_callback(btn):
    if btn == 'Main Screen':
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


########################################################################################################################
# Login Screen
########################################################################################################################

def login_form():
    global admin_login
    global user_login
    global my_id
    global login_username
    login_input = input_group("Login", [
        input('Username', name='username'),
        input('Password', type="password", name='password')])
    a = Login_User(None, login_input['username'], login_input['password'], False)
    a.login()
    login_username = a.username
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


########################################################################################################################
# Admin Panel and My Profile
########################################################################################################################

def admin_panel():
    put_html("<h1>Admin Panel</h1>")
    put_html("<h2>Application Configuration</h2>")
    config = session.query(Config).filter(Config.id == 1).one_or_none()
    put_table([
        ['Configuration Key', 'Configuration Value'],
        ['Location', config.city],
        ['Latitude', config.latitude],
        ['Longitude', config.longitude],
    ])
    put_button('Change', color="warning", onclick=lambda: body(edit_configuration)).style("align-self: center;")

    users = session.query(User).all()
    user_list = []

    for user in users:
        user_button = put_buttons(['Edit', 'Change Password', 'Delete'],
                                  onclick=lambda btn, user_id=user.id: users_buttons_callback(btn,
                                                                                              user_id)).style(
            "text-align: right; align-self: center;")
        user_data = [user.username, user.first_name, user.last_name, user_button]
        user_list.append(user_data)
    put_html("<h2>User Configuration</h2>")
    put_table(user_list, header=['Username', 'First Name', 'Last Name', 'Actions'])
    put_button('Add User', color="success", onclick=lambda: body(edit_user)).style("align-self: center;")


def edit_user(id=None):
    clear(scope='header')
    user = session.query(User).filter(User.id == id).one_or_none()
    if id == None:
        put_info("Leave Username or Password empty to skip creating user!")
        user_input = input_group("Add User", [
            input('Username', name='username', validate=check_user_input),
            input('Password', name='password'),
            input('First Name', name='first_name'),
            input('Last Name', name='last_name'),

        ])
        if user_input['username'] == "" or user_input['password'] == "":
            toast('Skipped Creating user 🔔')
        else:
            a = Update_User(None, user_input['username'],
                            hashlib.md5(user_input['password'].encode('utf-8')).hexdigest(), user_input['first_name'],
                            user_input['last_name'])
            a.create_user()
        body(admin_panel)
    else:
        user_input = input_group("Edit User", [
            input('Username', name='username', value=user.username, readonly=True),
            input('First Name', name='first_name', value=user.first_name),
            input('Last Name', name='last_name', value=user.last_name),

        ])
        a = Update_User(user.id, None, None, user_input['first_name'], user_input['last_name'])
        a.update_user()
        if my_id == 1:
            body(admin_panel)
        else:
            body(main_menu)


def edit_user_pass(id):
    clear(scope='header')
    user = session.query(User).filter(User.id == id).one_or_none()
    put_info("Leave empty to skip updating password...")
    user_input = input_group("Add or Edit User", [
        input('Password', name='password'),

    ])
    if user_input['password'] == "":
        toast('Skipped changing password 🔔')
    else:
        a = Update_User(user.id, None, hashlib.md5(user_input['password'].encode('utf-8')).hexdigest(), None, None)
        a.update_password()
        toast(user.username + ' new password is ' + str(user_input['password']) + ' 🔔')
    if my_id == 1:
        body(admin_panel)
    else:
        body(main_menu)


def edit_configuration():
    clear(scope='header')
    config = session.query(Config).filter(Config.id == 1).one_or_none()
    config_input = input_group("Edit Application Configuration", [
        input('Location', name='city', value=config.city, required=True),
        input('Latitude', name='latitude', value=config.latitude, required=True),
        input('Longitude', name='longitude', value=config.longitude, required=True),

    ])
    a = Update_Configuration(config_input['city'], config_input['latitude'].replace(',', '.'),
                             config_input['longitude'].replace(',', '.'))
    a.update_configuration()
    body(admin_panel)


def users_buttons_callback(btn, user_id):
    if btn == 'Delete':
        if user_id == 1:
            toast('Cannot Delete Admin User! 🔔')
        else:
            popup('Confirm User Deletion', [
                put_button('Confirm Deletion', color="danger", onclick=lambda: delete_user_handler(user_id))

            ])
    elif btn == 'Edit':
        body(edit_user, user_id)
    elif btn == 'Change Password':
        body(edit_user_pass, user_id)


def delete_user_handler(user_id):
    print('Delete ' + str(user_id))
    a = Update_User(user_id)
    a.delete_user()
    close_popup()
    toast('User Deleted! 🔔')
    body(admin_panel)


def check_user_input(input):
    user = session.query(User).filter(User.username == input).one_or_none()
    if user is not None:
        return 'Username already exists'


########################################################################################################################
# Pots
########################################################################################################################


def pots(id=None):
    put_html("<h1>My Pots</h1>")
    if id == None:
        # pots = session.query(Pot).options(joinedload(Pot.plant)).order_by(desc(Pot.id)).all()
        pots = session.query(Pot).order_by(desc(Pot.id)).all()
        put_button('Add New Pot', onclick=lambda: body(edit_pot), color="success").style(
            "text-align: right; align-self: center;")
    else:
        pots = session.query(Pot).filter(Pot.id == id)
    for pot in pots:
        if pot.plant_id == 0:
            pot_image = 'empty.png'
        else:
            pot_image = pot.plant.name + '.jpg'

        put_html("<h2>" + pot.name + " - " + pot.description + "</h2>")

        image_path = constant_plants_image_dir + pot_image

        if os.path.exists(image_path):
            img = open(image_path, 'rb').read()
        else:
            img = open(constant_plants_image_dir + 'empty.png', 'rb').read()


        put_row([
            put_image(img, format="png").style("margin: 0 auto; display: block; margin-bottom: 20px;"),
        ])
        if pot.plant_id != 0:
            last_measurement = session.query(Measurements).filter(Measurements.pot_id == pot.id).order_by(
                desc(Measurements.id)).first()
            table_html = f"""
                            <table style="margin: 0 auto; display: block; text-align: center;">
                                <tbody><tr>
                                    <th colspan="5" rowspan="1"><span style="white-space: pre-wrap;">{pot.plant.name}</span></th> 
                                </tr>
                                  <tr>
                                    <td colspan="5" rowspan="1"><span style="white-space: pre-wrap;">{pot.plant.description}</span></td> 
                                  </tr>
                                  <tr>
                                    <td><span style="white-space: pre-wrap;">Temp (°C)<br>{pot.plant.temperature_min} - {pot.plant.temperature_max}</span></td> 
                                    <td><span style="white-space: pre-wrap;">Light (lx)<br>{pot.plant.light_min} - {pot.plant.light_max}</span></td> 
                                    <td><span style="white-space: pre-wrap;">Humidity (%)<br>{pot.plant.soil_humidity_min} - {pot.plant.soil_humidity_max}</span></td> 
                                    <td><span style="white-space: pre-wrap;">pH<br>{pot.plant.soil_ph_min} - {pot.plant.soil_ph_max}</span></td> 
                                    <td><span style="white-space: pre-wrap;">Salinity (dS/m)<br>{pot.plant.soil_salinity_min} - {pot.plant.soil_salinity_max}</span></td> 
                                  </tr>
                                  <tr>
                                    <td><span style="white-space: pre-wrap;">{calculate_range_int(last_measurement.temperature, pot.plant.temperature_min, pot.plant.temperature_max, 1)}</span></td> 
                                    <td><span style="white-space: pre-wrap;">{calculate_range_int(last_measurement.light, pot.plant.light_min, pot.plant.light_max, 1)}</span></td> 
                                    <td><span style="white-space: pre-wrap;">{calculate_range_int(last_measurement.soil_hum, pot.plant.soil_humidity_min, pot.plant.soil_humidity_max, 1)}</span></td> 
                                    <td><span style="white-space: pre-wrap;">{calculate_range_float(last_measurement.soil_ph, pot.plant.soil_ph_min, pot.plant.soil_ph_max)}</span></td> 
                                    <td><span style="white-space: pre-wrap;">{calculate_range_float(last_measurement.soil_sal, pot.plant.soil_salinity_min, pot.plant.soil_salinity_max)}</span></td> 
                                  </tr>
                            </tbody></table><br>
                    """
            put_html(table_html)
            put_buttons(['Graphs', 'Edit', 'Sync with Sensor', 'Fix Plant', 'Change Plant', 'Detach Plant', 'Delete'],
                        onclick=lambda btn, pot_id=pot.id, pot_name=pot.name: pots_buttons_callback(btn,
                                                                                                    pot_id,
                                                                                                    pot_name)).style(
                "text-align: right; align-self: center;")
        else:
            table_html = f"""
                            <table style="margin: 0 auto; display: block; text-align: center;">
                                <tbody><tr>
                                    <th colspan="5" rowspan="1"><span style="white-space: pre-wrap;">Pot is empty!</span></th> 
                                </tr>
                            </tbody></table><br>
                    """
            put_html(table_html)
            put_buttons(['Edit', 'Attach Plant', 'Delete'],
                        onclick=lambda btn, pot_id=pot.id, pot_name=pot.name: pots_buttons_callback(btn,
                                                                                                    pot_id,
                                                                                                    pot_name)).style(
                "text-align: right; align-self: center;")


def calculate_range_int(measurement, measurement_min, measurement_max, step):
    if measurement in range(measurement_min, measurement_max + step):
        measurement_status = f"<p style='color: green;'>{str(measurement)} (OK)</p>"
    else:
        measurement_status = f"<p style='color: red;'>{str(measurement)} (Not OK)</p>"
    return measurement_status


def calculate_range_float(measurement, measurement_min, measurement_max):
    if measurement_min <= measurement <= measurement_max and round(measurement, 2) == measurement:
        measurement_status = f"<p style='color: green;'>{str(measurement)} (OK)</p>"
    else:
        measurement_status = f"<p style='color: red;'>{str(measurement)} (Not OK)</p>"
    return measurement_status


def edit_pot(id=None):
    clear(scope='header')
    pot = None
    header_input = "Add Pot"
    name_readonly = False
    if id is not None:
        pot = session.query(Pot).filter(Pot.id == id).one_or_none()
        header_input = "Edit Pot"
        name_readonly = True
    else:
        put_info("Leave Name empty to skip creating the Pot!")

    pot_input = input_group(header_input, [
        input('Name', name='name', value=pot.name if pot else '', readonly=name_readonly,
              validate=check_pot_input if not name_readonly else None),
        input('Description', name='description', value=pot.description if pot else ''),

    ])
    if pot_input['name'] == "":
        toast('Skipped creating Pot 🔔')
        body(pots)
    else:
        a = Update_Pot(id, pot_input['name'], pot_input['description'])
        if id is not None:
            a.update_pot()
            body(pots, pot.id)
        else:
            created_pot_id = a.create_pot()
            generate_measurement(created_pot_id)
            body(pots)


def edit_pot_attach(id, plant_id=None):
    if plant_id is None:
        clear(scope='header')
        plants = session.query(Plant).order_by(desc(Plant.id)).all()
        options = {plant.name: plant.id for plant in plants}
        options['Empty'] = 0
        selected_name = select('Select a plant:', options=options)
        selected_id = options[selected_name]
        b = Create_Measurements(None, id)
        b.delete_measurements()
        generate_measurement(id)
    else:
        selected_id = 0
    a = Update_Pot(id, None, None, selected_id, )
    a.attach_plant()
    body(pots, id)


def check_pot_input(input):
    pot = session.query(Pot).filter(Pot.name == input).one_or_none()
    if pot is not None:
        return 'Plant already exists'


def delete_pot_handler(pot_id, pot_name):
    b = Create_Measurements(None, pot_id)
    b.delete_measurements()
    a = Update_Pot(pot_id)
    a.delete_pot()
    close_popup()
    toast(pot_name + ' Deleted! 🔔')
    body(pots)


def pots_buttons_callback(btn, pot_id, pot_name):
    if btn == 'Attach Plant' or btn == 'Change Plant':
        body(edit_pot_attach, pot_id)
    elif btn == 'Detach Plant':
        body(edit_pot_attach, pot_id, 0)
    elif btn == 'Delete':
        popup('Confirm Pot Deletion', [
            put_button('Confirm ' + pot_name + ' Deletion', color="danger",
                       onclick=lambda: delete_pot_handler(pot_id, pot_name))

        ])
    elif btn == "Edit":
        body(edit_pot, pot_id)
    elif btn == "Sync with Sensor":
        generate_measurement(pot_id)
        body(pots, pot_id)
    elif btn == "Fix Plant":
        generate_measurement(pot_id, True)
        body(pots, pot_id)
    elif btn == "Graphs":
        plot_measurements(pot_id)


def generate_measurement(pot_id, fix_pot=False):
    if fix_pot:
        pot = session.query(Pot).filter(Pot.id == pot_id).one()
        temperature = random.randint(pot.plant.temperature_min, pot.plant.temperature_max)
        light = random.randint(pot.plant.light_min, pot.plant.light_max)
        soil_hum = random.randint(pot.plant.soil_humidity_min, pot.plant.soil_humidity_max)
        soil_ph = round(random.uniform(pot.plant.soil_ph_min, pot.plant.soil_ph_max), 2)
        soil_sal = round(random.uniform(pot.plant.soil_salinity_min, pot.plant.soil_salinity_max), 2)
    else:
        temperature = random.randint(10, 40)
        light = random.randint(1, 100)
        soil_hum = random.randint(10, 100)
        soil_ph = round(random.uniform(0.0, 14.0), 2)
        soil_sal = round(random.uniform(0.1, 5.8), 2)

    date = datetime.now() + timedelta(seconds=1)
    new_measurement = Measurements(
        date=date,
        pot_id=pot_id,
        temperature=temperature,
        light=light,
        soil_hum=soil_hum,
        soil_ph=soil_ph,
        soil_sal=soil_sal
    )
    session.add(new_measurement)
    session.commit()


########################################################################################################################
# Plants
########################################################################################################################

def plants(id=None):
    put_html("<h1>My Plants</h1>")
    if id == None:
        plants = session.query(Plant).order_by(desc(Plant.id)).all()
        put_button('Add New Plant', color="success", onclick=lambda: body(edit_plant)).style(
            "text-align: right; align-self: center;")
    else:
        plants = session.query(Plant).filter(Plant.id == id)
    for plant in plants:
        put_html("<h2>" + plant.name + " - " + plant.description + "</h2>")

        image_path = constant_plants_image_dir + plant.name + '.jpg'
        empty_image_path = constant_plants_image_dir + 'empty.png'

        if os.path.exists(image_path):
            img = open(image_path, 'rb').read()
        else:
            img = open(empty_image_path, 'rb').read()

        put_row([
            put_image(img, format="png").style("margin: 0 auto; display: block; margin-bottom: 20px;"),
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


def edit_plant(id=None):
    clear(scope='header')
    plant = None
    header_input = "Add Plant"
    name_readonly = False
    if id is not None:
        plant = session.query(Plant).filter(Plant.id == id).one_or_none()
        header_input = "Edit Plant"
        name_readonly = True
    else:
        put_info("Press Reset then Submit button to skip creating the Plant!")

    plant_input = input_group(header_input, [
        input('Name', name='name', value=plant.name if plant else '', readonly=name_readonly,
              validate=check_plant_input if not name_readonly else None),
        input('Description', name='description', value=plant.description if plant else ''),

        input('Minimum Temperature - \u00b0C', name='temp_min', value=plant.temperature_min if plant else '0',
              type=NUMBER, required=name_readonly, validate=check_plant_measurement),
        input('Maximum Temperature - \u00b0C', name='temp_max', value=plant.temperature_max if plant else '0',
              type=NUMBER, required=name_readonly, validate=check_plant_measurement),
        input('Minimum Light - lx', name='light_min', value=plant.light_min if plant else '0', type=NUMBER,
              required=name_readonly, validate=check_plant_measurement),
        input('Maximum Light - lx', name='light_max', value=plant.light_max if plant else '0', type=NUMBER,
              required=name_readonly, validate=check_plant_measurement),
        input('Minimum Humidity - %', name='hum_min', value=plant.soil_humidity_min if plant else '0', type=NUMBER,
              required=name_readonly, validate=check_plant_measurement),
        input('Maximum Humidity - %', name='hum_max', value=plant.soil_humidity_max if plant else '0', type=NUMBER,
              required=name_readonly, validate=check_plant_measurement),
        input('Minimum pH', name='ph_min', value=plant.soil_ph_min if plant else '0', type=FLOAT,
              required=name_readonly, validate=check_plant_measurement),
        input('Maximum pH', name='ph_max', value=plant.soil_ph_max if plant else '0', type=FLOAT,
              required=name_readonly, validate=check_plant_measurement),
        input('Minimum Salinity - dS/m', name='sal_min', value=plant.soil_salinity_min if plant else '0', type=FLOAT,
              required=name_readonly, validate=check_plant_measurement),
        input('Maximum Salinity - dS/m', name='sal_max', value=plant.soil_salinity_max if plant else '0', type=FLOAT,
              required=name_readonly, validate=check_plant_measurement)

    ])
    if plant_input['name'] == "":
        toast('Skipped creating Plant 🔔')
        body(plants)
    else:
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

def edit_plant_picture(id, name):
    clear(scope='header')
    put_info("Just press Submit without choosing file to skip changing image!")
    img = file_upload("Select a picture:", accept=".jpg", multiple=False, placeholder="Choose any .jpg file")

    if img is None:
        toast('Skipped changing image 🔔')
    else:
        output_dir = constant_plants_image_dir
        filename = os.path.join(output_dir, name + ".jpg")
        with open(filename, 'wb') as f:
            f.write(img['content'])

    body(plants, id)


def plants_buttons_callback(btn, plant_id, plant_name):
    if btn == 'Delete ' + plant_name:
        popup('Confirm Plant Deletion', [
            put_button('Confirm ' + plant_name + ' Deletion', color="danger",
                       onclick=lambda: delete_plant_handler(plant_id, plant_name))

        ])
    elif btn == 'Edit ' + plant_name:
        print('Edit ' + plant_name)
        body(edit_plant, plant_id)
    elif btn == 'Change Picture':
        body(edit_plant_picture, plant_id, plant_name)


def delete_plant_handler(plant_id, plant_name):
    a = Update_Plant(plant_id)
    a.delete_plant()
    image_path = constant_plants_image_dir + plant_name + '.jpg'
    if os.path.exists(image_path):
        os.remove(image_path)
    close_popup()
    toast(plant_name + ' Deleted! 🔔')
    body(plants)


def check_plant_input(input):
    plant = session.query(Plant).filter(Plant.name == input).one_or_none()
    if plant is not None:
        return 'Plant already exists'


def check_plant_measurement(input):
    if input is None:
        return 'Input cannot be none'


########################################################################################################################
# Plot Graphs
########################################################################################################################

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

    line = Plot("Line")
    line.set_options({
        "title": "Daily Min and Max Temperatures",
        "appendPadding": 32,
        "data": result,
        "xField": "time",
        "yField": "value",
        "seriesField": "type",
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
        },
        "height": 300,
    })

    put_html(line.render_notebook(), scope='main')


def plot_measurements(pot_id):
    last_10_desc = session.query(Measurements).filter_by(pot_id=pot_id).order_by(desc(Measurements.id)).limit(
        10).subquery()
    last_10_asc = session.query(last_10_desc).order_by(asc(last_10_desc.c.id)).subquery()
    data = session.query(last_10_asc).all()

    params_data = {}
    for measurement in data:
        date = measurement.date
        if date not in params_data:
            params_data[date] = {
                'temperature': [measurement.temperature],
                'light': [measurement.light],
                'soil_hum': [measurement.soil_hum],
                'soil_ph': [measurement.soil_ph],
                'soil_sal': [measurement.soil_sal]
            }
        else:
            params_data[date]['temperature'].append(measurement.temperature)
            params_data[date]['light'].append(measurement.light)
            params_data[date]['soil_hum'].append(measurement.soil_hum)
            params_data[date]['soil_ph'].append(measurement.soil_ph)
            params_data[date]['soil_sal'].append(measurement.soil_sal)

    dates = list(params_data.keys())
    temperature = [sum(params_data[date]['temperature']) / len(params_data[date]['temperature']) for date in dates]
    light = [sum(params_data[date]['light']) / len(params_data[date]['light']) for date in dates]
    soil_hum = [sum(params_data[date]['soil_hum']) / len(params_data[date]['soil_hum']) for date in dates]
    soil_ph = [sum(params_data[date]['soil_ph']) / len(params_data[date]['soil_ph']) for date in dates]
    soil_sal = [sum(params_data[date]['soil_sal']) / len(params_data[date]['soil_sal']) for date in dates]

    result = [{'time': date.strftime("%Y-%m-%d %H:%M:%S"), 'type': 'Temperature', 'value': temp} for date, temp in
              zip(dates, temperature)]

    result += [{'time': date.strftime("%Y-%m-%d %H:%M:%S"), 'type': 'Light', 'value': l} for date, l in
               zip(dates, light)]

    result += [{'time': date.strftime("%Y-%m-%d %H:%M:%S"), 'type': 'Soil Humidity', 'value': hum} for date, hum in
               zip(dates, soil_hum)]

    result += [{'time': date.strftime("%Y-%m-%d %H:%M:%S"), 'type': 'Soil pH', 'value': ph} for date, ph in
               zip(dates, soil_ph)]

    result += [{'time': date.strftime("%Y-%m-%d %H:%M:%S"), 'type': 'Soil Salinity', 'value': sal} for date, sal in
               zip(dates, soil_sal)]

    chart1 = Plot("Line")
    chart2 = Plot("Column")

    chart1.set_options({
        "title": f"Parameters over Time for Pot ID: {pot_id}",
        "data": result,
        "xField": "time",
        "yField": "value",
        "seriesField": "type",
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
        },
        "height": 400,
    })

    chart2.set_options({
        "title": f"Parameters over Time for Pot ID: {pot_id}",
        "data": result,
        "xField": "time",
        "yField": "value",
        "seriesField": "type",
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
        },
        "height": 400,
    })

    popup('Graph', [
        put_tabs([
            {'title': 'Line', 'content': put_html(chart1.render_notebook()).style("height: 500px;")},
            {'title': 'Bar', 'content': put_html(chart2.render_notebook()).style("height: 500px;")},
        ]),
        put_html("<br>"),
        put_button("Close", onclick=lambda: close_popup())
    ], size="large")


########################################################################################################################
# Start App
########################################################################################################################
put_scope('header', content=[header()])
put_scope('main', content=[body(login_form)])
