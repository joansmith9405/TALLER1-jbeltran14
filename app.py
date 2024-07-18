from flask import Flask , render_template , request, redirect , url_for
from dotenv import load_dotenv
from flask_login import login_manager , login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from db import db
from models.usuario import Usuario
from controller.perros_controller import PerrosController
from controller.saludos_controller import SaludosController
import os

load_dotenv()

#LLave generada, debe ser unica de cada usuario 
secret_key = os.urandom(24)
print(secret_key.hex())

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("USER_DB")}:{os.getenv("PASSWORD_DB")}@{os.getenv("HOST_DB")}/{os.getenv("SCHEMA_DB")}'
app.config["SECRET_KEY"] = secret_key
db.init_app(app)
api = Api(app)
login_manager = login_manager(app)
#db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    user = Usuario.query.get(user_id)


@app.route("/")
def main():
    return "Hello World"

@app.route("/login", methods =['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username,password=password).first()
        
        if user:
            login_user(user)
            if user.is_admin:
                return redirect(url_for("perroscontroller"))
            else:
                return redirect(url_for("saludoscontroller"))
            
    return render_template("login.html")        



api.add_resource(PerrosController, '/perros')
api.add_resource(SaludosController, '/saludos')