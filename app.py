import os
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, redirect, url_for, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dao.UsersDAO import UsersDAO
from dao.educationDAO import EducationDAO
from dao.languageDAO import LanguageDAO
from dao.projectDAO import ProjectDAO
from dao.skillDAO import SkillDAO
from dao.userProfileDAO import UserProfileDAO
from project_form import project_form
from portfolio import portfolio
from account import account
from signup import signup_user

app = Flask(__name__)

app.config.from_mapping(
	SECRET_KEY='secret_key_just_for_dev_environment',
	DATABASE=os.path.join(app.instance_path, 'todos.sqlite')
)

users_dao = UsersDAO()
education_dao = EducationDAO()
language_dao = LanguageDAO()
project_dao = ProjectDAO()
skill_dao = SkillDAO()
userProfile_DAO = UserProfileDAO()

UPLOAD_FOLDER = 'userpictures'  # Ordner für hochgeladene Bilder
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Erlaubte Dateitypen

# Home = Default
@app.route('/')
def index():
	return redirect(url_for('get_home'))


# Login Route # chatgpt-generated
@app.route('/login/', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_dao.check_user_credentials(email, password)

        if user:
            session['user_id'] = user.id
            return redirect(url_for('get_portfolio')) 
        else:
            return 'Invalid login credentials'
    return render_template('login.html')


# Home Route
@app.route('/home/')
def get_home():
    user_logged_in = 'user_id' in session
    user_first_name = None
    if user_logged_in:
        user_id = session['user_id']
        user_first_name = UsersDAO.get_user_first_name(user_id)
    return render_template('home.html', user_logged_in=user_logged_in, user_first_name=user_first_name)

# Account Route
@app.route('/account')
def get_account():
    return account()
    
# Logout Route
@app.route('/logout', methods=['POST'])
def get_logout():
    session.pop('user_id', None)
    return redirect(url_for('get_home'))

# FindJobs Route
@app.route('/findjobs/')
def get_findjobs():
	return render_template('findjobs.html') 

# MyPortfolio Route
@app.route('/portfolio/')
def get_portfolio():
    return portfolio()

# MyPortfolio Route
@app.route('/portfolio_edit/')
def get_portfolio_edit():
	return render_template('portfolio_edit_view.html') 

# ProjectForms Route
@app.route('/create_project/', methods=["GET", "POST"])
def get_project_form():
    return project_form()
   
# Signup Route
@app.route('/signup/', methods=["GET", "POST"])
def get_signup():
	return signup_user() 

@app.route("/submit", methods=["POST"])
def submit_project():
    return redirect("/portfolio/")

@app.route('/create_profile', methods=['POST'])
def create_user_profile_picture():
    picture = request.files['profile_picture']
    user_id = session['user_id']

    users_dao.create_user_profile(picture, user_id)
    return redirect(url_for('get_home'))



@app.route('/update_profile_picture', methods=['POST'])
def update_profile_picture():
    
    user_id = session['user_id']  # Annahme: Der angemeldete Benutzer ist in der Session gespeichert
    user_profile = userProfile_DAO.get_user_profile_by_user_id(user_id)

    if 'picture' in request.files:
        picture = request.files['picture']
        if picture and picture.filename != '' and allowed_file(picture.filename):
            filename = secure_filename(picture.filename)
            picture_path = os.path.join(UPLOAD_FOLDER, filename)
            picture.save(picture_path)

            if user_profile:
                userProfile_DAO.update_profile_picture(user_id, picture_path)
            else:
                userProfile_DAO.create_user_profile(user_id, "","", picture_path)

            return redirect(url_for('get_portfolio')) 

    return "Error updating profile picture"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# TEST ROUTE FÜR HTML SHIT MUSS ENTFERNT WERDEN AM ENDE
# ---
# ---
# ---
@app.route('/test/')
def portfolio_logged_in():
	return render_template('portfolio_logged_in.html') 
