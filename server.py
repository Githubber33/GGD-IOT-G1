from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__)

# Database configuratie
DB_HOST = "192.168.178.96" #mogelijk fout
DB_NAME = "temp"
DB_USER = "project-ggd"
DB_PASSWORD = "Webtech2025"

def get_temperature_data():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT recorded_at, temperature FROM public.sensor_data ORDER BY id DESC LIMIT 10;")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    data = get_temperature_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
