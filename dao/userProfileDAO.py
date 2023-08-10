import os
from werkzeug.utils import secure_filename

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databasetables.userProfile import UserProfile

# connect to database
DATABASE_URL = "sqlite:///jobfolio.db"
engine = create_engine(DATABASE_URL, echo=True)

# start session
Session = sessionmaker(bind=engine)
session = Session()

class UserProfileDAO:
    
    def create_user_profile(self, picture, title, short_description, user_id):
        
        # if-else chatgpt generated
        if picture:
            filename = secure_filename(picture.filename)
            picture.save(os.path.join('userpictures', filename))
        else:
            filename = None

    
        new_profile = UserProfile(
            picture=picture,
            title=title,
            short_description=short_description,
            user_id=user_id
        )
        session.add(new_profile)
        session.commit()
        return new_profile
    
    # chatgpt generated
    def update_profile_picture(self, user_id, picture_file):
        user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile:
            if picture_file:
                filename = secure_filename(picture_file.filename)
                picture_path = os.path.join('userpictures', filename)
                picture_file.save(picture_path)

                user_profile.picture = picture_path
                session.commit() 
                return user_profile
        return None


    @classmethod
    def get_user_profile_by_user_id(cls, user_id):
        user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()
        return user_profile

    
    # stuff for portfolio profile
        
    @classmethod
    def get_user_profile_picture(cls, user_id):
        user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile and user_profile.picture:
            return user_profile.picture
        else:
            return "{{ url_for('static', filename='default-pfp.jpg') }}"

    @classmethod
    def get_user_occupation(cls, user_id):
        user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile and user_profile.title:
            return user_profile.title
        else:
            return "Title not specified"

    @classmethod
    def get_user_description(cls, user_id):
        user_profile = session.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile and user_profile.short_description:
            return user_profile.short_description
        else:
            return "Description not available"
