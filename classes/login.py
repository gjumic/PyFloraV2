import hashlib

from classes.db_model import User
from database.Database import *

class Login_User():

    def __init__(self, id, username, password, login_status):
        self.id = id
        self.username = username
        self.password = password
        self.login_status = login_status

    def login(self):
        user = session.query(User).filter(User.username == self.username).one_or_none()
        if user is not None and hashlib.md5(self.password.encode('utf-8')).hexdigest() == user.password:
            self.id = user.id
            if user.username == "admin":
                self.login_status = "admin"
                return
            else:
                self.login_status = "user"