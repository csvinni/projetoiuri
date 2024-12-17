from flask import Flask, redirect, render_template, url_for, request, flash
import sqlite3
from models import User
from flask_login import LoginManager, login_user, login_required, logout_user
login_manager = LoginManager()

app = Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ULTRAMEGADIFICIL'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(usu_id):
    return User.get(usu_id)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = User.get_by_email(email)

        if usuario: 
            login_user(usuario)
            return redirect(url_for("dash"))
        else:
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/register",methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nome = request.form['nome']
        user = User(nome = nome, email = email, senha =senha)
        user.save()  

    return render_template("register.html")

@app.route("/dash")
@login_required
def dash():
    return render_template("dashboard.html")