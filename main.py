import network
import micropg_lite
import machine
import time

# === 📡 Wi-Fi instellingen ===
ssid = 'LT-Thijs'       # <-- Vervang dit met je echte Wi-Fi naam
password = 'ThijsGamesNL'  # <-- Vervang dit met je echte Wi-Fi wachtwoord

# === 🔖 Uniek device ID per Pico ===
device_id = "Reizigerkamer 1"   # <-- Verander dit voor elke nieuwe Pico (bv. pico_002, pico_003, etc.)


# VANAF hier hoef je niks te doen....

# === 🌐 Verbinden met Wi-Fi ===
print("Connecting to Wi-Fi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print("Wi-Fi connected:", wlan.ifconfig())

# === 🗄️ Verbinden met PostgreSQL database ===
print("Connecting to PostgreSQL database...")
try:
    conn = micropg_lite.connect(
        host='139.162.160.244',    # <-- Jouw cloud server IP of hostname
        user='project-ggd',           # <-- Jouw databasegebruikersnaam
        password='Webtech2025',   # <-- Jouw databasewachtwoord
        database='temp'    # <-- Naam van jouw database
    )
    print("Database connection successful.")
except Exception as e:
    print("Database connection failed:", e)
    raise

cur = conn.cursor()

# === 🌡️ Temperatuur uitlezen functie ===
def read_internal_temperature():
    print("Reading internal temperature...")
    adc = machine.ADC(4)  # Interne sensor (GPIO 4)
    raw_value = adc.read_u16()
    voltage = (raw_value / 65535) * 3.3
    temperature = (voltage - 0.5) * 100
    print(f"Raw: {raw_value}, Temp: {temperature:.2f}°C")
    return round(temperature, 2)

# === 🔁 Loop: Elke 10s temperatuur loggen ===
try:
    while True:
        start_time = time.time()
        temperature = read_internal_temperature()

        print("Inserting data into database...")
        try:
            cur.execute(
                'INSERT INTO sensor_data (temperature, device_id) VALUES (%s, %s)',
                (str(temperature), device_id)
            )
            conn.commit()
            print(f"Data inserted: {temperature}°C - {device_id}")
        except Exception as e:
            print("Error inserting data:", e)
        

        # Wachten tot volgende meting
        sleep_time = 5 - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    conn.close()
    print("Database connection closed.")

