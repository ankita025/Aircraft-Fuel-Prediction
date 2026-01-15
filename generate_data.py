import pandas as pd
import random
from datetime import datetime, timedelta

# Aircraft types list
aircraft_types = ["Boeing 737", "Airbus A320", "Boeing 747", "Airbus A380",
                  "Boeing 777", "Cessna 172", "Embraer E190", "ATR 72"]

# Generate 150 rows of data
rows = []
start_date = datetime(2010, 1, 1)

for _ in range(150):
    aircraft = random.choice(aircraft_types)
    distance = random.randint(200, 10000)  # km
    payload = random.randint(500, 25000)  # kg
    altitude = random.randint(5000, 40000)  # ft
    speed = random.randint(200, 950)  # km/h
    temperature = random.randint(-10, 35)  # °C
    wind_speed = random.randint(5, 120)  # km/h
    humidity = random.randint(10, 90)  # %
    duration = round(distance / speed + random.uniform(0.5, 2), 2)  # hours

    # Fuel consumption logic
    if "Cessna" in aircraft:
        factor = 0.9
    elif "747" in aircraft:
        factor = 1.6
    elif "A380" in aircraft:
        factor = 1.4
    elif "ATR" in aircraft:
        factor = 1.5
    elif "Embraer" in aircraft:
        factor = 1.3
    elif "777" in aircraft:
        factor = 1.3
    else:
        factor = 1.35

    fuel = int(distance * factor + payload * 0.2 + wind_speed * 2 - temperature * 3)

    # Assign random year based on date range
    random_date = start_date + timedelta(days=random.randint(0, 365 * 15))
    year = random_date.year

    rows.append([aircraft, distance, payload, altitude, speed, temperature, wind_speed, humidity, duration, fuel, year])

# Create DataFrame
df = pd.DataFrame(rows, columns=[
    "aircraft_type", "distance_km", "payload_kg", "altitude_ft",
    "cruise_speed_kmh", "temperature_c", "wind_speed_kmh",
    "humidity_percent", "flight_duration_hr", "fuel_liters", "year"
])

# Save CSV
df.to_csv("aircraft_fuel_data.csv", index=False)
print("150 rows generated and saved in aircraft_fuel_data.csv!")
