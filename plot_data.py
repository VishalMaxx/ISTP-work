import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("data/rainfall_data_shimla_25.csv")

# Rename columns for sanity (optional but recommended)
df = df.rename(columns={
    "Data Acquisition Time": "datetime",
    "Telemetry Hourly Rainfall (mm)": "rainfall_mm"
})

# Convert datetime column (day-first format)
df["datetime"] = pd.to_datetime(
    df["datetime"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"   # invalid rows become NaT
)

# Convert rainfall to numeric
df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")

# Drop rows with invalid datetime or rainfall
df = df.dropna(subset=["datetime", "rainfall_mm"])

# Sort by time (VERY IMPORTANT for time series)
df = df.sort_values("datetime")

# Plot
plt.figure(figsize=(12, 5))
plt.plot(df["datetime"], df["rainfall_mm"], color="red", linewidth=2)

# Labels and title
plt.xlabel("Time")
plt.ylabel("Hourly Rainfall (mm)")
plt.title("Hourly Rainfall Time Series")

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Grid for clarity
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
