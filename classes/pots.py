from classes.db_model import Pot
from database.Database import *


class Update_Pot():

    def __init__(self, id, name=None, description=None, plant_id=None, temperature=None, light=None, soil_hum=None,
                 soil_ph=None, soil_sal=None):
        self.name = name
        self.description = description
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

        session.commit()

    def attach_plant(self):
        print("Update Pot with id: " + str(self.id))
        pot = session.query(Pot).filter(Pot.id == self.id).one_or_none()
        pot.plant_id = self.plant_id

        session.commit()

    def delete_pot(self):
        print("Delete Pot with id: " + str(self.id))
        session.query(Pot).filter(Pot.id == self.id).delete()
        session.commit()

    def create_pot(self):
        print("Create Pot: " + self.name)
        new_pot = Pot(name=self.name, description=self.description, temperature=0, light=0, soil_hum=0, soil_ph=0,
                      soil_sal=0, plant_id=0)

        session.add(new_pot)
        session.commit()
