from classes.db_model import Pot
from database.Database import *


class Delete_Pot():

    def __init__(self, id):
        self.id = id

    def delete_pot(self):
        print("Delete Pot with id: " + str(self.id))
        session.query(Pot).filter(Pot.id == self.id).delete()
        session.commit()

class Update_Pot():

    def __init__(self, id, name, description, status, plant_id, temperature, light, soil_hum, soil_ph, soil_sal):
        self.name = name
        self.description = description
        self.status = status
        self.plant_id = plant_id
        self.temperature = temperature
        self.light = light
        self.soil_hum = soil_hum
        self.soil_ph = soil_ph
        self.soil_sal = soil_sal
        self.id = id

    def update_pot(self):
        print("Update Pot with id: " + str(self.id))
        pot = session.query(Pot).filter(Pot.id == self.id).one_or_none()
        pot.name = self.name
        pot.description = self.description
        pot.status = self.status
        pot.plant_id = self.plant_id
        pot.temperature = self.temperature
        pot.light = self.light
        pot.soil_hum = self.soil_hum
        pot.soil_ph = self.soil_ph
        pot.soil_sal = self.soil_sal

        session.commit()