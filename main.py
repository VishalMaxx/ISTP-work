import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Load CSV files
# =========================
rain_df = pd.read_csv("data\\rainfall_data_shimla_25.csv")
river_df = pd.read_csv("data\\river_discharge_shimla_25.csv")

# =========================
# Rename columns
# =========================
rain_df = rain_df.rename(columns={
    "Data Acquisition Time": "datetime",
    "Telemetry Hourly Rainfall (mm)": "rainfall_mm"
})

river_df = river_df.rename(columns={
    "Data Acquisition Time": "datetime",
    "Telemetry Hourly River Water Discharge (m3/sec)": "discharge_m3s"
})

# =========================
# Convert datetime
# =========================
rain_df["datetime"] = pd.to_datetime(
    rain_df["datetime"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

river_df["datetime"] = pd.to_datetime(
    river_df["datetime"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)

# =========================
# Convert numeric values
# =========================
rain_df["rainfall_mm"] = pd.to_numeric(rain_df["rainfall_mm"], errors="coerce")
river_df["discharge_m3s"] = pd.to_numeric(river_df["discharge_m3s"], errors="coerce")

# =========================
# Drop invalid rows
# =========================
rain_df = rain_df.dropna(subset=["datetime", "rainfall_mm"])
river_df = river_df.dropna(subset=["datetime"])

# =========================
# Sort by time
# =========================
rain_df = rain_df.sort_values("datetime")
river_df = river_df.sort_values("datetime")

# =========================
# Create common time index
# =========================
merged_df = pd.merge(
    rain_df[["datetime", "rainfall_mm"]],
    river_df[["datetime", "discharge_m3s"]],
    on="datetime",
    how="outer"
).sort_values("datetime")

# =========================
# Plot with dual y-axis
# =========================
fig, ax1 = plt.subplots(figsize=(13, 6))

# Rainfall (RED)
ax1.plot(
    merged_df["datetime"],
    merged_df["rainfall_mm"],
    color="red",
    linewidth=2,
    label="Rainfall (mm)"
)
ax1.set_xlabel("Time")
ax1.set_ylabel("Rainfall (mm)", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# River Discharge (BLUE)
ax2 = ax1.twinx()
ax2.plot(
    merged_df["datetime"],
    merged_df["discharge_m3s"],
    color="blue",
    linewidth=2,
    label="River Discharge (m³/s)"
)
ax2.set_ylabel("River Discharge (m³/s)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

# =========================
# Final formatting
# =========================
plt.title("Rainfall vs River Discharge (Lag Effect Visible)")
fig.autofmt_xdate()
plt.grid(True)
plt.tight_layout()
plt.show()
