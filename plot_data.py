import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Define data folder path
data_folder = Path(__file__).parent / "data"

# Read rainfall data
rainfall_file = data_folder / "rainfall_data_shimla_25.csv"
rainfall_df = pd.read_csv(rainfall_file)

# Read river discharge data
discharge_file = data_folder / "river_discharge_shimla_25.csv"
discharge_df = pd.read_csv(discharge_file)

# Convert datetime columns
rainfall_df['Data Acquisition Time'] = pd.to_datetime(rainfall_df['Data Acquisition Time'], format='%d-%m-%Y %H:%M')
discharge_df['Data Acquisition Time'] = pd.to_datetime(discharge_df['Data Acquisition Time'], format='%d-%m-%Y %H:%M')

# Sort by datetime
rainfall_df = rainfall_df.sort_values('Data Acquisition Time')
discharge_df = discharge_df.sort_values('Data Acquisition Time')

# Create plots
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: Rainfall over time
ax1 = axes[0]
rainfall_values = rainfall_df['Telemetry Hourly Rainfall (mm)'].values
times = rainfall_df['Data Acquisition Time'].values
ax1.plot(times, rainfall_values, linewidth=1, color='blue', alpha=0.7)
ax1.set_xlabel('Date and Time')
ax1.set_ylabel('Rainfall (mm)')
ax1.set_title('Hourly Rainfall Data - Shimla')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Plot 2: River discharge over time
ax2 = axes[1]
# Replace 'NaN' strings with actual NaN and convert to numeric
discharge_df['Telemetry Hourly River Water Discharge (m3/sec)'] = pd.to_numeric(
    discharge_df['Telemetry Hourly River Water Discharge (m3/sec)'], 
    errors='coerce'
)
discharge_values = discharge_df['Telemetry Hourly River Water Discharge (m3/sec)'].dropna().values
discharge_times = discharge_df[discharge_df['Telemetry Hourly River Water Discharge (m3/sec)'].notna()]['Data Acquisition Time'].values

ax2.plot(discharge_times, discharge_values, linewidth=1, color='green', alpha=0.7)
ax2.set_xlabel('Date and Time')
ax2.set_ylabel('River Discharge (m³/sec)')
ax2.set_title('Hourly River Discharge Data - Shimla')
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(data_folder.parent / 'rainfall_discharge_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved to: rainfall_discharge_plot.png")
plt.show()

# Print basic statistics
print("\n=== Rainfall Data Summary ===")
print(f"Total records: {len(rainfall_df)}")
print(f"Date range: {rainfall_df['Data Acquisition Time'].min()} to {rainfall_df['Data Acquisition Time'].max()}")
print(f"Rainfall statistics (mm):")
print(rainfall_df['Telemetry Hourly Rainfall (mm)'].describe())

print("\n=== River Discharge Data Summary ===")
print(f"Total records: {len(discharge_df)}")
discharge_values_numeric = pd.to_numeric(discharge_df['Telemetry Hourly River Water Discharge (m3/sec)'], errors='coerce')
print(f"Date range: {discharge_df['Data Acquisition Time'].min()} to {discharge_df['Data Acquisition Time'].max()}")
print(f"River discharge statistics (m³/sec):")
print(discharge_values_numeric.describe())
