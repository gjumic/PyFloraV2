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
        input('Username', name='username'),
        input('Password', type="password", name='password')])
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


def body(body_function):
    clear(scope='header')
    header()
    clear(scope='main')
    try:
        with use_scope('main'):
            return body_function()
    except Exception as e:
        print(e)
    finally:
        footer()
    # with use_scope('main', clear=True):
    #     return body_function()

def main_buttons_callback(btn):
    if btn == 'Main Menu':
        body(graf)
    elif btn == 'Logout':
        body(logout)
    elif btn == 'Admin Panel':
        body(admin_panel)

def header():
    with use_scope('header', clear=True):
        put_image(img, format="png").style("align-self: center;")
        if admin_login:
            put_buttons(['Main Menu', 'Admin Panel','Logout'], onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")
        if user_login:
            # put_button("Main Menu", onclick=lambda: body(graf), color='success', outline=True).style(
            #     "text-align: right; align-self: center;")
            # put_button("Logout", onclick=lambda: body(logout), color='success', outline=True).style(
            #     "text-align: right; align-self: center;")
            put_buttons(['Main Menu', 'Logout'], onclick=lambda btn: main_buttons_callback(btn)).style(
                "text-align: right; align-self: center;")


def footer():
    # remove(scope='footer')
    with use_scope('footer', clear=True):
        put_text("Made by Goran Jumić")


def admin_panel():
    put_text("admin panel content")


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
