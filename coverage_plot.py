import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Read database
conn = sqlite3.connect("muon_data.db")

df = pd.read_sql_query("""
SELECT experiment,
       theta_center,
       momentum
FROM muon_data
WHERE theta_center IS NOT NULL
  AND momentum IS NOT NULL
""", conn)

conn.close()

# Marker styles (one per experiment)
markers = {
    "DEIS": "o",
    "MUTRON": "s",
    "AMH": "^",
    "Kiel-DESY": "D",
    "OKAYAMA": "v",
    "De Pascale": "P",
    "Kellogg": "X",
    "L3+C": "<",
    "Nottingham": ">"
}

fig, ax = plt.subplots(figsize=(10, 7))

for experiment, group in df.groupby("experiment"):
    ax.scatter(
        group["momentum"],
        group["theta_center"],
        marker=markers[experiment],
        s=45,
        alpha=0.75,
        edgecolors="black",
        linewidth=0.4,
        label=experiment,
    )

ax.set_xscale("log")
ax.set_xlabel("Momentum (GeV/$c$)")
ax.set_ylabel("Zenith angle (degrees)")
ax.set_title("Coverage of Atmospheric Muon Measurements")

ax.set_ylim(0, 90)
ax.grid(True, which="both", linestyle=":", alpha=0.5)

ax.legend(title="Experiment", fontsize=9)

plt.tight_layout()
plt.show()