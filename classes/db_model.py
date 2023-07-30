import hashlib



from database.Database import *
from database.MySetup import Base
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String, nullable=False, unique=True)
    password = db.Column("password", db.String, nullable=False, unique=False)
    first_name = db.Column("first_name", db.String, nullable=True, unique=False)
    last_name = db.Column("last_name", db.String, nullable=True, unique=False)
    city = db.Column("city", db.String, nullable=False, unique=False)
    active = db.Column("active", db.Boolean)

class Plant(Base):
    __tablename__ = "plants"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, nullable=False, unique=True)
    description = db.Column("description", db.String, nullable=True, unique=False)
    image = db.Column("image", db.String, nullable=True, unique=False)

    temperature_min = db.Column("temperature_min", db.Integer, nullable=False, unique=False)
    temperature_max = db.Column("temperature_max", db.Integer, nullable=False, unique=False)

    light_min = db.Column("light_min", db.Integer, nullable=False, unique=False)
    light_max = db.Column("light_max", db.Integer, nullable=False, unique=False)

    soil_humidity_min = db.Column("soil_humidity_min", db.Float, nullable=False, unique=False)
    soil_humidity_max = db.Column("soil_humidity_max", db.Float, nullable=False, unique=False)

    soil_ph_min = db.Column("soil_ph_min", db.Float, nullable=False, unique=False)
    soil_ph_max = db.Column("soil_ph_max", db.Float, nullable=False, unique=False)

    soil_salinity_min = db.Column("soil_salinity_min", db.Float, nullable=False, unique=False)
    soil_salinity_max = db.Column("soil_salinity_max", db.Float, nullable=False, unique=False)

class Pot(Base):
    __tablename__ = "pots"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String, nullable=False, unique=True)
    description = db.Column("description", db.String, nullable=True, unique=False)
    status = db.Column("status", db.String, nullable=False, unique=False, default='empty')
    plant_id = db.Column("plant_id", db.Integer, ForeignKey('plants.id'))

    temperature = db.Column("temperature", db.Integer, nullable=False, unique=False)
    light = db.Column("light", db.Integer, nullable=False, unique=False)
    soil_hum = db.Column("soil_hum", db.Float, nullable=False, unique=False)
    soil_ph = db.Column("soil_ph", db.Float, nullable=False, unique=False)
    soil_sal = db.Column("soil_sal", db.Float, nullable=False, unique=False)

class Login_User():

    def __init__(self, username, password, login_status):
        self.username = username
        self.password = password
        self.login_status = login_status

    def login(self):
        user = session.query(User).filter(User.username == self.username).one_or_none()
        if user is not None and hashlib.md5(self.password.encode('utf-8')).hexdigest() == user.password:
            if user.username == "admin":
                self.login_status = "admin"
                return
            else:
                self.login_status = "user"