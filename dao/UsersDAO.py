
# chatgpt generated

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databasetables.users import User 

# Verbindung zur SQLite-Datenbank herstellen
DATABASE_URL = "sqlite:///jobfolio.db"
engine = create_engine(DATABASE_URL, echo=True)

# Session erstellen
Session = sessionmaker(bind=engine)
session = Session()

class UsersDAO:

    @classmethod
    def check_user_credentials(email, password):
        user = session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            return user 
        else:
            return None

    @classmethod
    def logout(self):
        session.close()

    @classmethod
    def create_user(cls, first_name, last_name, email, phone_number, street, zipcode, city, password):
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            street=street,
            zipcode=zipcode,
            city=city,
            password=password
        )
        session.add(new_user)
        session.commit()
        return new_user