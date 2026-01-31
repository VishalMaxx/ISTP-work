import pandas as pd
import matplotlib.pyplot as plt

# Read rainfall CSV
rain_df = pd.read_csv("data/rainfall_data_shimla_25.csv")

# Rename column for clarity
rain_df.rename(columns={"Telemetry Hourly Rainfall (mm)": "Rainfall_mm"}, inplace=True)

# Convert time column to datetime
rain_df["Data Acquisition Time"] = pd.to_datetime(
    rain_df["Data Acquisition Time"], format="%d-%m-%Y %H:%M"
)

# Keep only required columns
rain_df = rain_df[["Data Acquisition Time", "Rainfall_mm"]]

# Sort by time (important for plotting)
rain_df = rain_df.sort_values("Data Acquisition Time")

# Create plot
fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    rain_df["Data Acquisition Time"],
    rain_df["Rainfall_mm"],
    width=0.03,
    label="Rainfall (mm)"
)

ax.set_xlabel("Time")
ax.set_ylabel("Rainfall (mm)")
ax.set_title("Hourly Rainfall – Bagi Gumma")

fig.autofmt_xdate()
ax.legend()

plt.tight_layout()
plt.show()
# Save figure (headless-safe)
# plt.savefig("rainfall_only.png", dpi=300, bbox_inches="tight")
# plt.close()
