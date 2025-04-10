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
    cursor.execute("""
        SELECT mac_address, recorded_at, temperature 
        FROM public.sensor_data 
        WHERE mac_address IS NOT NULL
        ORDER BY recorded_at DESC LIMIT 100;
    """)
    rows = cursor.fetchall()
    conn.close()

    # # Groepeer per MAC
    data_by_mac = {}
    for mac, time, temp in rows:
        if mac not in data_by_mac:
            data_by_mac[mac] = []
        data_by_mac[mac].append({"time": time.isoformat(), "temperature": float(temp)})

    return data_by_mac


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_temperature_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
