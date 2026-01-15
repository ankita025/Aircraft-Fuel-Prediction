import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("aircraft_fuel_data.csv")

# Rename column to match our model
df.rename(columns={"fuel_liters":"fuel"}, inplace=True)

# One-hot encode
df = pd.get_dummies(df, columns=["aircraft_type"])

X = df.drop("fuel", axis=1)
y = df["fuel"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
print("\nMAE:", round(mean_absolute_error(y_test, pred),2))
print("RMSE:", round(mean_squared_error(y_test, pred)**0.5,2))
print("R2:", round(r2_score(y_test, pred),2))

# Save model
pickle.dump(model, open("fuel_model.pkl","wb"))

# Save columns (important for Flask)
pickle.dump(X.columns, open("model_columns.pkl","wb"))

print("\nModel + Columns saved successfully! ✔️")
