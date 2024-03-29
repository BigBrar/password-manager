from flask import Flask, render_template, request, redirect, session
import generate_password
from db_interactions import add_pass, verify_user, find_user, get_pass, edit_pass, delete_pass
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta
from flask_login import UserMixin
from wtforms.validators import InputRequired,  Length, ValidationError

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/deep/flask-projects/password_manager/database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)
app.app_context().push()
user = ""

# app.secret_key = 'dw@G*YmrDat'
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(minutes=10000)  
serializer = URLSafeTimedSerializer('dw@G*YmrDat')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    

def check_user(username,password):
    user = User.query.filter_by(username=username).first()
    return user

def add_user(username,email,password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print("user added....")

def check_login(username, entered_password):
    try:
        user = User.query.filter_by(username=username).first()
    # print(user.password)
        if user.password == entered_password:
            return True
        else:
            return False
    except:
        return False

def generate_token(user_id,password):
    data = {'id':user_id,'password':password}
    return serializer.dumps(data)

def generate_hash(password):
    password_hash = bcrypt.generate_password_hash(password)
    return password_hash

def check_hash(password_hash, password):
    result = bcrypt.check_password_hash(password_hash,password)
    return result

def decode_token(token):
    try:
        data = serializer.loads(token,max_age=600)
        return data
    except:
        return None


@app.route('/',methods=['GET'])
def main_page():
    try:
        if 'token' in session:
            global user
            token_data = decode_token(session['token'])
            id = token_data['id']
            user = id
            print(f'USER - {id}')
            password = token_data['password']
            print('token exists')
            verify_user(id)
            user_data = get_pass(id)
            print(f'ID - {id} PASSWORD - {password}')
            return render_template('index.html',list = user_data)
        return redirect('/login')
    except Exception as e:
        print(e)
        return redirect('/login')

@app.route('/create_pass',methods=['POST'])
def another_func():
    if request.method == 'POST':
        print("ENVOKED ROUTE    ")
        account_name = request.form['account']
        username = request.form['username']
        email = request.form['email']
        note = request.form['note']
        if username == "" and email == "":
            return 'Username or email is required...'
        elif account_name == "":
            return 'account name is required'
        password = generate_password.create_pass(10)
        print("CALLED FUNCTION..")
        add_pass(user, username, email, account_name
        , password, note)
        return redirect('/')
    else:
        return "INVALID method used..."
    

@app.route('/edit_pass',methods=['POST'])
def test_nothing():
    print("I WAS CALLED....")
    # token_data = decode_token(session['token'])
    # user = token_data['id']
    global user
    loop_index = request.form['loopIndex']
    account_name = request.form['account']
    username = request.form['username']
    email = request.form['email']
    note = request.form['note']
    password = request.form['password-field']
    edit_pass(int(loop_index), user, account_name, username, email, note,password)
    return redirect('/')

@app.route('/delete',methods=['POST'])
def delete_data():
    global user
    data = request.get_json()
    index = data.get('index') 
    if delete_pass(user, int(index)):
        return render_template('index.html')
    return "something went wrong..."



@app.route('/login',methods=['POST','GET'])
def login_attempt():
    if request.method == 'POST':
        # email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user_exists = check_login(username,password)
        print("Result ->",user_exists)
        if user_exists:
            session['token'] = generate_token(username,password)
            session.permanent = True
            return redirect('/')
        else:
            return "username or password is incorrect..."
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register_urself():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(email, username, password )
        user = check_user(username,password)
        if user:
            return "Username already exists..."
        else:
            add_user(username,email,password)
            session['token'] = generate_token(username,password)
            session.permanent = True
            return redirect('/')
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)