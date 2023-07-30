import sqlalchemy as db
from sqlalchemy.orm import sessionmaker



db_engine = db.create_engine('sqlite:///database/database.db')
db_connection = db_engine.connect()
Session = sessionmaker()
Session.configure(bind=db_engine)
session = Session()