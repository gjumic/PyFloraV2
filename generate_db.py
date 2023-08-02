import hashlib

import database.MySetup
from classes import db_model
from database.Database import *
import random
from datetime import datetime, timedelta

database.MySetup.Base.metadata.create_all(bind=db_engine)

city = "Osijek"
latitude = 45.55
longitude = 18.69

new_config = db_model.Config(city=city, latitude=latitude, longitude=longitude)
session.add(new_config)

user_data = [
    ("admin", hashlib.md5("2241".encode('utf-8')).hexdigest(), "Administrator", ""),
    ("goran", hashlib.md5("2310".encode('utf-8')).hexdigest(), "Goran", "Jumic"),
    ("pero", hashlib.md5("2310".encode('utf-8')).hexdigest(), "Pero", ""),
]

plant_data = [
    ("Rose", "Beautiful red flowers", 10, 30, 8, 80, 20, 80, 5.5, 7.0, 0.1, 0.5),
    ("Lavender", "Fragrant purple flowers", 5, 25, 8, 60, 20, 100, 6.0, 7.5, 0.1, 0.6),
    ("Snake Plant", "Tall green leaves", 15, 35, 5, 40, 30, 100, 5.5, 7.5, 0.1, 0.7),
    ("Fern", "Lush green foliage", 18, 25, 8, 100, 40, 10, 5.0, 6.5, 0.1, 0.6),
    ("Cactus", "Spiny desert plant", 20, 40, 1, 120, 10, 70, 6.5, 8.0, 0.1, 0.8),
    ("Orchid", "Elegant and delicate flowers", 18, 30, 15, 80, 30, 80, 5.5, 6.5, 0.1, 0.7),
    ("Spider Plant", "Green and white striped leaves", 15, 28, 5, 40, 20, 90, 5.8, 7.2, 0.1, 0.6),
    ("Bamboo", "Fast-growing tall plant", 20, 35, 8, 50, 20, 90, 6.0, 7.5, 0.1, 0.7),
    ("Succulent", "Water-storing fleshy leaves", 15, 30, 5, 60, 10, 60, 6.0, 7.5, 0.1, 0.7),
    ("Aloe Vera", "Soothing gel-filled leaves", 20, 35, 5, 40, 20, 80, 5.5, 7.0, 0.1, 0.6),
]

pot_data = [
    ("Pot 1", "Small clay pot", 1),
    ("Pot 2", "Terracotta pot", 2),
    ("Pot 3", "Ceramic pot", 3),
    ("Pot 4", "Plastic pot", 4),
    ("Pot 5", "Glass pot", 5),
    ("Pot 6", "Metal pot", 6),
    ("Pot 7", "Wooden pot", 7),
    ("Pot 8", "Cement pot", 8),
    ("Pot 9", "Plastic pot", 9),
    ("Pot 10", "test pot", 0),
    ("Pot 11", "Terracotta pot", 10),
]

def generate_random_measurements(pot_id, start_date, num_measurements):
    measurements = []
    for i in range(num_measurements):
        date = start_date + timedelta(days=i)
        temperature = random.randint(10, 40)
        light = random.randint(1, 100)
        soil_hum = random.randint(10, 100)
        soil_ph = round(random.uniform(0.0, 14.0), 2)
        soil_sal = round(random.uniform(0.1, 5.8), 2)
        measurements.append((date, pot_id, temperature, light, soil_hum, soil_ph, soil_sal))  # Fix the order of elements here
    return measurements

start_date = datetime(2023, 7, 25)
num_measurements_per_pot = 5

measurement_data = (
    generate_random_measurements(1, start_date, num_measurements_per_pot),
    generate_random_measurements(2, start_date, num_measurements_per_pot),
    generate_random_measurements(3, start_date, num_measurements_per_pot),
    generate_random_measurements(4, start_date, num_measurements_per_pot),
    generate_random_measurements(5, start_date, num_measurements_per_pot),
    generate_random_measurements(6, start_date, num_measurements_per_pot),
    generate_random_measurements(7, start_date, num_measurements_per_pot),
    generate_random_measurements(8, start_date, num_measurements_per_pot),
    generate_random_measurements(9, start_date, num_measurements_per_pot),
    generate_random_measurements(10, start_date, num_measurements_per_pot),
    generate_random_measurements(11, start_date, num_measurements_per_pot)
)

for record in user_data:
    username, password, first_name, last_name = record
    new_user = db_model.User(username=username, password=password, first_name=first_name, last_name=last_name)
    session.add(new_user)

for record in plant_data:
    name, description, temp_min, temp_max, light_min, light_max, hum_min, hum_max, ph_min, ph_max, sal_min, sal_max = record
    new_plant = db_model.Plant(name=name, description=description, temperature_min=temp_min, temperature_max=temp_max,
                               light_min=light_min, light_max=light_max, soil_humidity_min=hum_min,
                               soil_humidity_max=hum_max,
                               soil_ph_min=ph_min, soil_ph_max=ph_max, soil_salinity_min=ph_min,
                               soil_salinity_max=ph_max)
    session.add(new_plant)

for record in pot_data:
    name, description, plant_id = record
    new_pot = db_model.Pot(name=name, description=description,plant_id=plant_id)

    session.add(new_pot)

for measurement_list in measurement_data:
    for record in measurement_list:
        date, pot_id, temperature, light, soil_hum, soil_ph, soil_sal = record
        new_measurement = db_model.Measurements(
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
