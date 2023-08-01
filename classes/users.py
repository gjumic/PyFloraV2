from classes.db_model import User
from database.Database import *


class Update_User():

    def __init__(self, id, username=None, password=None, first_name=None, last_name=None):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def create_user(self):
        print("Create User: " + self.username)
        username = self.username
        password = self.password
        first_name = self.first_name
        last_name = self.last_name
        new_user = User(username=username, password=password, first_name=first_name, last_name=last_name)

        session.add(new_user)
        session.commit()

    def update_user(self):
        print("Update User with id: " + str(self.id))
        user = session.query(User).filter(User.id == self.id).one_or_none()
        user.first_name = self.first_name
        user.last_name = self.last_name

        session.commit()

    def update_password(self):
        print("Update User Password with id: " + str(self.id))
        user = session.query(User).filter(User.id == self.id).one_or_none()
        user.password = self.password

        session.commit()

    def delete_user(self):
        print("Delete User with id: " + str(self.id))
        session.query(User).filter(User.id == self.id).delete()

        session.commit()
