import os
import time
from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    # 12-Factor: Environment variables se config read karna
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Ek simple query chala kar check karte hain
            cursor.execute("SELECT VERSION() AS version;")
            result = cursor.fetchone()
        connection.close()
        return jsonify({
            "status": "Success",
            "message": "Hello Dosto! Connected to 2-Tier DB successfully.",
            "db_version": result['version']
        })
    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": f"Database se connect nahi ho paya: {str(e)}"
        }), 500

if __name__ == '__main__':
    # 12-Factor: Port binding via env variable
    port = int(os.environ.get('FLASK_APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port)