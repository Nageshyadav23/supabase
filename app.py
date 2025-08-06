# pip install psycopg2-binary flask_sqlalchmey : use %40 inplace of "@"

from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your actual credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Foodrescue%402025@db.nqucecczthnqttuguvfc.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model matching the Supabase table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.String(50))

@app.route('/')
def index():
    return 'welcome'

# @app.route('/insert')
# def insert():
#     new_user = User(id=2,name='shushmitha', email='sh@gmail.com')
#     db.session.add(new_user)
#     db.session.commit()
#     return 'User added'


# 📄 GET /users — Fetch all users
@app.route('/selectuser', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'name': u.name, 'email': u.email}
        for u in users
    ])

# ➕ POST /users — Add a new user
@app.route('/createuser', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(id=data['id'],name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return "user created"

# ✏️ PUT /users/<id> — Update user details
@app.route('/updateuser/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    user.name = data.get('name')
    user.email = data.get('email')
    db.session.commit()
    return "user updated"

# # ❌ DELETE /users/<id> — Delete user
@app.route('/deleteuser/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return "deleted successfully"


if __name__ == '__main__':
    app.run(debug=True)
