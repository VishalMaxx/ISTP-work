import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Load data
# =========================
rain_df = pd.read_csv("data/Rainfall_2021_2023.csv")
river_df = pd.read_csv("data/Water_Discharge_2021_2023.csv")

# =========================
# Parse datetime (mixed formats!)
# =========================
rain_df["datetime"] = pd.to_datetime(
    rain_df["Data Acquisition Time"], dayfirst=True, errors="coerce"
)
river_df["datetime"] = pd.to_datetime(
    river_df["Data Acquisition Time"], dayfirst=True, errors="coerce"
)

# =========================
# Numeric conversion
# =========================
rain_df["rainfall_mm"] = pd.to_numeric(rain_df["rainfall_mm"], errors="coerce")
river_df["discharge_m3s"] = pd.to_numeric(river_df["discharge_m3s"], errors="coerce")

# =========================
# Clean
# =========================
rain_df = rain_df.dropna(subset=["datetime", "rainfall_mm"])
river_df = river_df.dropna(subset=["datetime", "discharge_m3s"])

rain_df = rain_df.sort_values("datetime")
river_df = river_df.sort_values("datetime")

# =========================
# Event-based window (KEY)
# =========================
rain_events = rain_df[rain_df["rainfall_mm"] > 0]

start = rain_events["datetime"].min() - pd.Timedelta(days=3)
end   = rain_events["datetime"].max() + pd.Timedelta(days=5)

rain_zoom = rain_df[(rain_df["datetime"] >= start) & (rain_df["datetime"] <= end)]
river_zoom = river_df[(river_df["datetime"] >= start) & (river_df["datetime"] <= end)]

# =========================
# Plot
# =========================
fig, ax1 = plt.subplots(figsize=(14, 6))

# ---- Rainfall as RED LINE (step-style) ----
ax1.plot(
    rain_zoom["datetime"],
    rain_zoom["rainfall_mm"],
    color="red",
    linewidth=2,
    drawstyle="steps-post",
    label="Rainfall (mm)"
)
ax1.set_ylabel("Rainfall (mm)", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# ---- River discharge as BLUE LINE ----
ax2 = ax1.twinx()
ax2.plot(
    river_zoom["datetime"],
    river_zoom["discharge_m3s"],
    color="blue",
    linewidth=2.5,
    label="River Discharge (m³/s)"
)
ax2.set_ylabel("River Discharge (m³/s)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

# =========================
# Formatting
# =========================
plt.title("Rainfall–Runoff Response (Clear Lag Visualization)")
fig.autofmt_xdate()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

