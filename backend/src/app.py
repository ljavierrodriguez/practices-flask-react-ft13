from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Profile, Role, RoleUser
import datetime

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '455a0595071af6e2385c0ec556cb329c'
db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email")
        password = request.json.get("password")

        if not email: return jsonify({"email": "Email is required!"}), 422
        if not password: return jsonify({"password": "Password is required!"}), 422

        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({ "faild": "Email/Password are incorrect!"}), 401
        if not check_password_hash(user.password, password): return jsonify({ "faild": "Email/Password are incorrect!"}), 401

        expire = datetime.timedelta(minutes=1)
        access_token = create_access_token(identity=user.email, expires_delta=expire)

        date = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(date)
        expire_date = datetime.datetime.fromtimestamp(timestamp + expire.total_seconds())
        
        data = {
            "access_token": access_token,
            "expire_date": expire_date,
            "user": user.serialize_with_roles()
        }

        return jsonify(data), 200



@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def users(id = None):
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.serialize_with_roles(), users))
        return jsonify(users), 200

    if request.method == 'POST':
        
        email = request.json.get("email")
        password = request.json.get("password")
        name = request.json.get("name", "")
        lastname = request.json.get("lastname", "")
        biography = request.json.get("biography", "")
        roles = request.json.get("roles", [2])

        user_exist = User.query.filter_by(email=email).first()
        if user_exist: return jsonify({ "error": "user already exists!"}), 400

        user = User()
        user.email = email
        user.password = generate_password_hash(password)
        #user.active = True
        #user.save()

        profile = Profile()
        profile.name = name
        profile.lastname = lastname
        profile.biography = biography
        #profile.user_id = user.id
        #profile.save()
        for role in roles:
            role = Role.query.get(role)
            user.roles.append(role)

        user.profile = profile
        user.save()

        return jsonify(user.serialize_with_roles()), 201


    if request.method == 'PUT':
        
        email = request.json.get("email")
        password = request.json.get("password")
        name = request.json.get("name", "")
        lastname = request.json.get("lastname", "")
        biography = request.json.get("biography", "")
        roles = request.json.get("roles", [2])

        user_exist = User.query.filter_by(email=email).first()
        if user_exist.id != id: return jsonify({ "error": "user already exists!"}), 400

        user = User.query.get(id)
        if not user: return jsonify({ "error": "user doesn't exist!"}), 404

        user.email = email
        user.password = generate_password_hash(password)
        user.profile.name = name
        user.profile.lastname = lastname
        user.profile.biography = biography
        user.update()

        return jsonify(user.serialize_with_roles()), 201

    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: return jsonify({ "error": "user doesn't exist!"}), 404
        user.delete()
        return jsonify({ "success": "User was deleted!"}), 200




if __name__ == '__main__':
    app.run()