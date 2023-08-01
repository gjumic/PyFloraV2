import hashlib

import database.MySetup
from classes import db_model
from database.Database import *

database.MySetup.Base.metadata.create_all(bind=db_engine)

city = "Osijek"

new_config = db_model.Config(city=city)
session.add(new_config)

user_data = [
    ("admin", hashlib.md5("2241".encode('utf-8')).hexdigest(), "", ""),
    ("goran", hashlib.md5("2310".encode('utf-8')).hexdigest(), "Goran", "Jumic"),
    ("pero", hashlib.md5("2310".encode('utf-8')).hexdigest(), "Pero", ""),
]

plant_data = [
    ("Rose", "Beautiful red flowers", "rose.jpg", 10, 30, 1000, 8000, 20, 80, 5.5, 7.0, 0.1, 0.5),
    ("Lavender", "Fragrant purple flowers", "lavender.jpg", 5, 25, 800, 6000, 20, 100, 6.0, 7.5, 0.1, 0.6),
    ("Snake Plant", "Tall green leaves", "snake_plant.jpeg", 15, 35, 500, 4000, 30, 100, 5.5, 7.5, 0.1, 0.7),
    ("Fern", "Lush green foliage", "fern.jpg", 18, 25, 800, 3000, 40, 10, 5.0, 6.5, 0.1, 0.6),
    ("Cactus", "Spiny desert plant", "cactus.jpg", 20, 40, 1000, 12000, 10, 70, 6.5, 8.0, 0.1, 0.8),
    ("Orchid", "Elegant and delicate flowers", "orchid.jpg", 18, 30, 1500, 8000, 30, 80, 5.5, 6.5, 0.1, 0.7),
    ("Spider Plant", "Green and white striped leaves", "spider_plant.jpg", 15, 28, 500, 4000, 20, 90, 5.8, 7.2, 0.1, 0.6),
    ("Bamboo", "Fast-growing tall plant", "bamboo.jpg", 20, 35, 800, 5000, 20, 90, 6.0, 7.5, 0.1, 0.7),
    ("Succulent", "Water-storing fleshy leaves", "succulent.jpg", 15, 30, 500, 6000, 10, 60, 6.0, 7.5, 0.1, 0.7),
    ("Aloe Vera", "Soothing gel-filled leaves", "aloe_vera.jpg", 20, 35, 500, 4000, 20, 80, 5.5, 7.0, 0.1, 0.6),
]

pot_data = [
    ("Pot 1", "Small clay pot", "occupied", 25, 6000, 0.6, 6.8, 0.3, 1),
    ("Pot 2", "Terracotta pot", "occupied", 20, 4000, 0.8, 7.2, 0.2, 2),
    ("Pot 3", "Ceramic pot", "empty", 22, 5000, 0.7, 6.5, 0.1, 3),
    ("Pot 4", "Plastic pot", "occupied", 18, 800, 0.9, 6.0, 0.4, 4),
    ("Pot 5", "Glass pot", "empty", 24, 2000, 0.5, 6.2, 0.1, 5),
    ("Pot 6", "Metal pot", "empty", 28, 3000, 0.4, 7.0, 0.2, 6),
    ("Pot 7", "Wooden pot", "occupied", 22, 1500, 0.7, 5.8, 0.2, 7),
    ("Pot 8", "Cement pot", "empty", 20, 3500, 0.6, 6.5, 0.3, 8),
    ("Pot 9", "Plastic pot", "occupied", 18, 400, 0.5, 6.5, 0.3, 9),
    ("Pot 10", "Terracotta pot", "empty", 23, 3000, 0.7, 6.8, 0.2, 10),
]

for record in user_data:
    username, password, first_name, last_name = record
    new_user = db_model.User(username=username, password=password, first_name=first_name, last_name=last_name)
    session.add(new_user)

for record in plant_data:
    name, description, image, temp_min, temp_max, light_min, light_max, hum_min, hum_max, ph_min, ph_max, sal_min, sal_max = record
    new_plant = db_model.Plant(name=name, description=description, image=image, temperature_min=temp_min, temperature_max=temp_max,
                      light_min=light_min, light_max=light_max, soil_humidity_min=hum_min, soil_humidity_max=hum_max,
                      soil_ph_min=ph_min, soil_ph_max=ph_max, soil_salinity_min=ph_min, soil_salinity_max=ph_max)
    session.add(new_plant)

for record in pot_data:
    name, description, status, temp, light, soil_hum, soil_ph, soil_sal, plant_id = record
    new_pot = db_model.Pot(name=name, description=description, status=status,
                  temperature=temp, light=light, soil_hum=soil_hum, soil_ph=soil_ph, soil_sal=soil_sal, plant_id=plant_id)
    session.add(new_pot)

session.commit()