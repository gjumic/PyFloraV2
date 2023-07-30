from classes.db_model import *

user = "goran"
password = "2310"

a = Login_User(user, password, False)
a.login()

if a.login_status == "admin":
    print('Admin Login! 🔔')
    admin_login = True
elif a.login_status == "user":
    print('Login OK! 🔔')
    user_login = True
else:
    print('Login Failed! 🔔')