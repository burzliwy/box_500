from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from sqlite_handler import sql
from redis_server import RedisServer
from static.modules.game import Game
import uuid


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


db = sql()
db.create_table()
redis = RedisServer()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)
    
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user[1] if user else None

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.get_user(identity)


# ROUTES

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/organizer/<organizer_id>/dashboard')
def organizer_dashboard(organizer_id):
    return render_template('organizer_dashboard.html', organizer_id=organizer_id)

@app.route('/game/<game_id>')
def game(game_id):
    return render_template('game.html', game_id=game_id)

@app.route('/organizer/<organizer_id>/game/edit/<game_id>')
def edit_game(organizer_id, game_id):
    return render_template('edit_game.html', organizer_id=organizer_id, game_id=game_id)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return render_template('protected.html', username=current_user)







# API ROUTES

@app.route('/organizer/<organizer_id>/create-game', methods=['POST'])
def create_game(organizer_id):
    if request.method == 'POST':
        game_name = 'test'  
        game_id = str(uuid.uuid4())
        game = Game(game_id, game_name)
        redis.set_game(game_id, game)
        return game_id, game_name
    
@app.route('/auth', methods=['POST'])
def auth():
    db.get_connection()
    if request.is_json:
        username = request.json.get('username')
        password = request.json.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    user = db.get_user(username)
    if user is None:
        return jsonify({"msg": "User not found"}), 401
    if user[2] != password:
        return jsonify({"msg": "Invalid password"}), 401
    
    db.close()

    access_token = create_access_token(identity=username)
    
    response = make_response(jsonify({
        "msg": "Login successful",
        "access_token": access_token,
        "username": username
    }))
    response.set_cookie('access_token', access_token)
    return response

@app.route('/register/auth', methods=['POST'])
def register_auth():
    db.get_connection()
    if request.is_json:
        username = request.json.get('username')
        password = request.json.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    user = db.get_user(username)
    if user is not None:
        return jsonify({"msg": "User already exists"}), 400
    
    db.create_user(username, password)
    db.close()
    
    access_token = create_access_token(identity=username)



    return render_template('index.html', username=username, access_token=access_token)







# WEBSOCKETS









if __name__ == '__main__':
    app.run(debug=True)


