import os
import time
from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

# Ek table banane ke liye function (12-Factor: Bootstrapping)
def init_db():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE
            );
        """)
    connection.commit()
    connection.close()

# Pehli baar table banane ke liye call karenge
try:
    init_db()
except Exception as e:
    print(f"Database init fail ho gaya (paise hi hota hai jab DB ready na ho): {e}")

@app.route('/')
def index():
    return jsonify({
        "status": "Success",
        "message": "Welcome! Naya data add karne ke liye /add par jayein aur dekhne ke liye /users par."
    })

# 1. DATA ADD KARNE KA ROUTE
@app.route('/add')
def add_user():
    # Hum sample ke liye URL parameters se data lenge: /add?name=Lavkesh&email=lavkesh@test.com
    name = request.args.get('name', 'Naya Dosto')
    email = request.args.get('email', f"user_{int(time.time())}@test.com") # Unique email ke liye timestamp
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))
        connection.commit()
        connection.close()
        
        return jsonify({
            "status": "Success",
            "message": f"User {name} successfully database mein add ho gaya hai!"
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

# 2. DATA DEKHNE KA ROUTE
@app.route('/users')
def get_users():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
        connection.close()
        return jsonify({
            "status": "Success",
            "total_users": len(users),
            "users_list": users
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port)