from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

DATA_FILE = "aircraft_fuel_data.csv"
df = pd.read_csv(DATA_FILE)

@app.route("/")
def home():
    df = pd.read_csv(DATA_FILE)

    summary = {
        "total_fuel": int(df["fuel_liters"].sum()),
        "total_flights": len(df),
        "aircraft_count": df["aircraft_type"].nunique()
    }

    return render_template("index.html", summary=summary)

@app.route("/predict", methods=["POST"])
def predict():
    aircraft = request.form["aircraft_type"]
    distance = float(request.form["distance"])
    payload = float(request.form["payload"])
    speed = float(request.form["speed"])
    altitude = float(request.form["altitude"])
    temperature = float(request.form["temperature"])
    wind = float(request.form["wind"])

    # Base fuel rate (liters per km)
    base_rates = {
        "Airbus A320": 3.5,
        "Boeing 737": 3.8,
        "Boeing 747": 9.5,
        "Boeing 777": 8.0,
        "Airbus A380": 10.5,
        "Embraer E190": 2.8,
        "ATR 72": 2.2,
        "Cessna 172": 0.9
    }

    base = base_rates.get(aircraft, 3.5)

    # Simple fuel estimation logic
    fuel = (
        distance * base +
        payload * 0.002 +
        wind * 5 -
        temperature * 2 +
        altitude * 0.0005
    )

    fuel = int(max(fuel, 0))

    return render_template(
        "index.html",
        fuel=fuel
    )

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    df = pd.read_csv(DATA_FILE)

    fuel_by_aircraft = (
        df.groupby("aircraft_type")["fuel_liters"]
        .sum()
        .to_dict()
    )

    return render_template(
        "dashboard.html",
        fuel_by_aircraft=fuel_by_aircraft
    )

@app.route("/admin")
def admin():
    import pandas as pd

    df = pd.read_csv("aircraft_fuel_data.csv")

    stats = {
        "total_fuel": int(df["fuel_liters"].sum()),
        "total_flights": len(df),
        "avg_fuel": int(df["fuel_liters"].mean())
    }

    yearly_fuel = (
        df.groupby("year")["fuel_liters"]
        .sum()
        .to_dict()
    )

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        yearly_fuel=yearly_fuel
    )

# =========================
# YEARLY REPORT
# =========================
@app.route("/yearly")
def yearly():
    df = pd.read_csv(DATA_FILE)

    yearly_data = (
        df.groupby("year")["fuel_liters"]
        .sum()
        .to_dict()
    )

    return render_template(
        "yearly.html",
        yearly_data=yearly_data
    )


# =========================
# ANALYTICS
# =========================
@app.route("/analytics")
def analytics():
    df = pd.read_csv(DATA_FILE)

    analytics_data = (
        df.groupby("aircraft_type")
        .agg(
            avg_fuel=("fuel_liters", "mean"),
            avg_distance=("distance_km", "mean"),
            flights=("aircraft_type", "count")
        )
        .reset_index()
        .to_dict(orient="records")
    )

    return render_template(
        "analytics.html",
        analytics=analytics_data
    )


# =========================
# HISTORY
# =========================
@app.route("/history")
def history():
    df = pd.read_csv(DATA_FILE)

    records = df.tail(200).to_dict(orient="records")

    return render_template(
        "history.html",
        records=records
    )



# ---------- AIRCRAFT FLEET ----------
@app.route("/aircraft")
def aircraft():
    aircrafts = sorted(df["aircraft_type"].unique())
    return render_template("aircraft_list.html", aircrafts=aircrafts)

# ---------- AIRCRAFT DETAIL ----------
@app.route("/aircraft/<name>")
def aircraft_detail(name):
    d = df[df["aircraft_type"] == name]
    if d.empty:
        return "Aircraft not found", 404

    return render_template(
        "aircraft_detail.html",
        aircraft=name,
        total_fuel=int(d["fuel_liters"].sum()),
        avg_fuel=round(d["fuel_liters"].mean(), 2),
        avg_distance=round(d["distance_km"].mean(), 2),
        flights=len(d),
        yearly=d.groupby("year")["fuel_liters"].sum().to_dict()
    )

# ---------- COMPARE ----------
@app.route("/compare")
def compare():
    df = pd.read_csv("aircraft_fuel_data.csv")

    aircrafts = sorted(df["aircraft_type"].unique())

    a1 = request.args.get("a1")
    a2 = request.args.get("a2")
    route = request.args.get("route")

    comparison = None
    better_aircraft = None
    route_recommendation = None

    if a1 and a2:
        df1 = df[df["aircraft_type"] == a1]
        df2 = df[df["aircraft_type"] == a2]

        if not df1.empty and not df2.empty:
            comparison = {
                "a1": {
                    "fuel": int(df1["fuel_liters"].sum()),
                    "distance": int(df1["distance_km"].sum()),
                    "flights": int(len(df1))
                },
                "a2": {
                    "fuel": int(df2["fuel_liters"].sum()),
                    "distance": int(df2["distance_km"].sum()),
                    "flights": int(len(df2))
                }
            }

            # 🏆 Better aircraft (lower fuel/km)
            a1_eff = comparison["a1"]["fuel"] / comparison["a1"]["distance"]
            a2_eff = comparison["a2"]["fuel"] / comparison["a2"]["distance"]
            better_aircraft = a1 if a1_eff < a2_eff else a2

            # 🛫 Route-based recommendation
            avg_dist_a1 = comparison["a1"]["distance"] / comparison["a1"]["flights"]
            avg_dist_a2 = comparison["a2"]["distance"] / comparison["a2"]["flights"]

            if route == "short":
                route_recommendation = a1 if avg_dist_a1 < avg_dist_a2 else a2
            elif route == "medium":
                route_recommendation = a1 if abs(avg_dist_a1-2500) < abs(avg_dist_a2-2500) else a2
            elif route == "long":
                route_recommendation = a1 if avg_dist_a1 > avg_dist_a2 else a2

    return render_template(
        "compare.html",
        aircrafts=aircrafts,
        comparison=comparison,
        better_aircraft=better_aircraft,
        route_recommendation=route_recommendation
    )


# ---------- EFFICIENCY ----------
@app.route("/efficiency")
def efficiency():
    ranking = (
        df.groupby("aircraft_type")
        .apply(lambda x: x["fuel_liters"].sum() / x["distance_km"].sum())
        .reset_index(name="fuel_per_km")
        .sort_values("fuel_per_km")
        .to_dict(orient="records")
    )
    return render_template("efficiency.html", ranking=ranking)

# ---------- MAINTENANCE ----------
@app.route("/maintenance")
def maintenance():
    insights = (
        df.assign(fuel_per_hr=df["fuel_liters"] / df["flight_duration_hr"])
        .groupby("aircraft_type")["fuel_per_hr"]
        .mean()
        .reset_index()
        .sort_values("fuel_per_hr", ascending=False)
        .to_dict(orient="records")
    )
    return render_template("maintenance.html", insights=insights)

# ---------- CEO ----------
@app.route("/ceo")
def ceo():
    summary = {
        "total_fuel": int(df["fuel_liters"].sum()),
        "total_flights": len(df),
        "aircraft_types": df["aircraft_type"].nunique(),
        "years": f"{df['year'].min()} - {df['year'].max()}"
    }
    return render_template("ceo.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=False)
