from classes.db_model import Config
from database.Database import *

class Update_Configuration():

    def __init__(self, city=None, latitude=None, longitude=None):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude

    def update_configuration(self):
        config = session.query(Config).filter(Config.id == 1).one_or_none()
        config.city = self.city
        config.latitude = self.latitude
        config.longitude = self.longitude

        session.commit()

    def get_configuration(self):
        config = session.query(Config).filter(Config.id == 1).one_or_none()
        self.city = config.city
        self.latitude = config.latitude
        self.longitude = config.longitude