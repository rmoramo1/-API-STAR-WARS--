"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes, Favoritos
#from models import Person

#import JWT for tokenization
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# config for jwt
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Inician los POST************************************************************************************************************

@app.route('/login', methods=['POST']) 
def login():
    mail = request.json.get("mail", None)
    password = request.json.get("password", None)

    print(mail)
    print(password)

    user = User.query.filter_by(mail=mail, password=password).first()
    # valida si estan vacios los ingresos
    if user is None:
       return jsonify({"msg": "Bad mail or password"}), 401
    
    # crear token login
    access_token = create_access_token(identity=mail)
    return jsonify({"token": access_token})

@app.route('/user', methods=['POST'])
def register_user():
    name = request.json.get("name", None)
    mail = request.json.get("mail", None)
    password = request.json.get("password", None)

    # valida si estan vacios los ingresos
    if name is None:
        return jsonify({"msg": "No Name was provided"}), 400
    if mail is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    
    # busca usuario en BBDD
    user = User.query.filter_by(mail=mail).first()
     # the user was not found on the database
    if user:
        return jsonify({"msg": "User already exists"}), 401
    else:
        # crea usuario nuevo
        # crea registro nuevo en BBDD de 
        user1 = User(name=name, mail=mail, password=password)
        db.session.add(user1)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 200

@app.route('/personajes', methods=['POST']) 
def register_personajes():
    name = request.json.get("name", None)
    gender = request.json.get("gender", None)
    hair_color = request.json.get("hair_color", None)
    eye_color = request.json.get("eye_color", None)

    # valida si estan vacios los ingresos
    if name is None:
        return jsonify({"msg": "No Name was provided"}), 400
    if gender is None:
        return jsonify({"msg": "No gender was provided"}), 400
    if hair_color is None:
        return jsonify({"msg": "No hair_color was provided"}), 400
    if eye_color is None:
        return jsonify({"msg": "No eye_color was provided"}), 400

    # busca usuario en BBDD
    personajes = Personajes.query.filter_by(name=name, gender=gender, hair_color=hair_color, eye_color=eye_color).first()
    if personajes:
        return jsonify({"msg": "Personajes already exists"}), 401
    # the user was not found on the database
    else:
        # crea personajes nuevo
        # crea registro nuevo en BBDD de 
        personajes1 = Personajes(name=name, gender=gender, hair_color=hair_color, eye_color=eye_color)
        db.session.add(personajes1)
        db.session.commit()
        return jsonify({"msg": "Personajes created successfully"}), 200

@app.route('/planetas', methods=['POST']) 
def regiter_planetas():
    name = request.json.get("name", None)
    diameter = request.json.get("diameter", None)
    population = request.json.get("population", None)
    terrain = request.json.get("terrain", None)

    if name is None:
        return jsonify({"msg": "No Name was provided"}), 400
    if diameter is None:
        return jsonify({"msg": "No diameter was provided"}), 400
    if population is None:
        return jsonify({"msg": "No population was provided"}), 400
    if terrain is None:
        return jsonify({"msg": "No terrain was provided"}), 400

    # busca usuario en BBDD
    planetas = Planetas.query.filter_by(name=name, diameter=diameter, population=population, terrain=terrain).first()
    
    # the user was not found on the database
    if planetas:
        return jsonify({"msg": "planetas already exists"}), 401
    else:
        # crea planeta nuevo
        # crea registro nuevo en BBDD de
        planetas1 = Planetas(name=name, diameter=diameter, population=population, terrain=terrain)
        db.session.add(planetas1)
        db.session.commit()
        return jsonify({"msg": "planetas created successfully"}), 200

#Inician los GET***********************************************************************************************************

@app.route('/user', methods = ['GET'])
def users():
    if request.method == 'GET':
        records = User.query.all()
        return jsonify([User.serialize(record) for record in records]) #LLAMAR A TODOS
    else:
        return jsonify({"msg": "no autorizado"})

#SOLO MANDA A LLAMAR A UNO SOLO 
@app.route('/user/<user>/', methods = ['GET'])
def user(user):
    if request.method == 'GET':
        records = User.query.filter_by(id=user)  #FILTRA SOLAMENTE EL ID
        return jsonify([User.serialize(record) for record in records])
    else:
        return jsonify({"msg": "no autorizado"})

@app.route('/personajes', methods = ['GET'])
def personajes():
    if request.method == 'GET':
        records = Personajes.query.all()
        return jsonify([Personajes.serialize(record) for record in records]) #LLAMAR A TODOS
    else:
        return jsonify({"msg": "no autorizado"})

#SOLO MANDA A LLAMAR A UNO SOLO 
@app.route('/personajes/<personaje>/', methods = ['GET'])
def personaje(personaje):
    if request.method == 'GET':
        records = Personajes.query.filter_by(id=personaje)  #FILTRA SOLAMENTE EL ID
        return jsonify([Personajes.serialize(record) for record in records])
    else:
        return jsonify({"msg": "no autorizado"})

@app.route('/planetas', methods = ['GET'])
def planetas():
    if request.method == 'GET':
        records = Planetas.query.all()
        return jsonify([Planetas.serialize(record) for record in records]) #LLAMAR A TODOS
    else:
        return jsonify({"msg": "no autorizado"})

#SOLO MANDA A LLAMAR A UNO SOLO 
@app.route('/planetas/<planeta>/', methods = ['GET'])
def planeta(planeta):
    if request.method == 'GET':
        records = Planetas.query.filter_by(id=planeta)  #FILTRA SOLAMENTE EL ID
        return jsonify([Planetas.serialize(record) for record in records])
    else:
        return jsonify({"msg": "no autorizado"})

#SOLO MANDA A LLAMAR A UNO SOLO 
@app.route('/favoritos/<favorito>/', methods = ['GET'])
def favorito(favorito):
    if request.method == 'GET':
        records = Favoritos.query.filter_by(id=favorito)  #FILTRA SOLAMENTE EL ID
        return jsonify([Favoritos.serialize(record) for record in records])
    else:
        return jsonify({"msg": "no autorizado"})

#Inician los DELETE***********************************************************************************************************

@app.route("/favoritos/<favorito>", methods=["DELETE"])
def favorito_delete(favorito):
    favorito = Favoritos.query.get(favorito)
    db.session.delete(favorito)
    db.session.commit()
    return "Favoritos was successfully deleted"


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
