from classes.db_model import Measurements
from database.Database import *


class Create_Measurements():

    def __init__(self, id, pot_id, date=None, temperature=None, light=None, soil_hum=None, soil_ph=None,
                 soil_sal=None):
        self.id = id
        self.date = date
        self.pot_id = pot_id
        self.temperature = temperature
        self.light = light
        self.soil_hum = soil_hum
        self.soil_ph = soil_ph
        self.soil_sal = soil_sal

    def create_measurement(self):
        new_pot = Measurements(date=self.date, pot_id=self.pot_id, temperature=self.temperature, light=self.light,
                               soil_hum=self.soil_hum, soil_ph=self.soil_ph,
                               soil_sal=0)

        session.add(new_pot)
        session.commit()

    def delete_measurements(self):
        print("Delete Measurement where pot id: " + str(self.pot_id))
        session.query(Measurements).filter(Measurements.pot_id == self.pot_id).delete()
        session.commit()
