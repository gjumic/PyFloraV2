from classes.db_model import Plant
from database.Database import *


class Update_Plant():

    def __init__(self, id, name=None, description=None, temperature_min=0, temperature_max=0, light_min=0, light_max=0,
                 soil_humidity_min=0, soil_humidity_max=0, soil_ph_min=0, soil_ph_max=0, soil_salinity_min=0,
                 soil_salinity_max=0):
        self.id = id
        self.name = name
        self.description = description
        self.temperature_min = temperature_min
        self.temperature_max = temperature_max
        self.light_min = light_min
        self.light_max = light_max
        self.soil_humidity_min = soil_humidity_min
        self.soil_humidity_max = soil_humidity_max
        self.soil_ph_min = soil_ph_min
        self.soil_ph_max = soil_ph_max
        self.soil_salinity_min = soil_salinity_min
        self.soil_salinity_max = soil_salinity_max

    def update_plant(self):
        print("Update Plant with id: " + str(self.id))
        print("Update Plant with name: " + str(self.name))
        plant = session.query(Plant).filter(Plant.id == self.id).one_or_none()
        plant.name = self.name
        plant.description = self.description
        plant.temperature_min = self.temperature_min
        plant.temperature_max = self.temperature_max
        plant.light_min = self.light_min
        plant.light_max = self.light_max
        plant.soil_humidity_min = self.soil_humidity_min
        plant.soil_humidity_max = self.soil_humidity_max
        plant.soil_ph_min = self.soil_ph_min
        plant.soil_ph_max = self.soil_ph_max
        plant.soil_salinity_min = self.soil_salinity_min
        plant.soil_salinity_max = self.soil_salinity_max

        session.commit()

    def delete_plant(self):
        print("Delete Plant with id: " + str(self.id))
        session.query(Plant).filter(Plant.id == self.id).delete()

        session.commit()

    def create_plant(self):
        print("Create Plant: " + self.name)
        new_plant = Plant(name=self.name, description=self.description,
                          temperature_min=self.temperature_min, temperature_max=self.temperature_max,
                          light_min=self.light_min, light_max=self.light_max,
                          soil_humidity_min=self.soil_humidity_min, soil_humidity_max=self.soil_humidity_max,
                          soil_ph_min=self.soil_ph_min, soil_ph_max=self.soil_ph_max,
                          soil_salinity_min=self.soil_salinity_min, soil_salinity_max=self.soil_salinity_max
                          )

        session.add(new_plant)
        session.commit()
