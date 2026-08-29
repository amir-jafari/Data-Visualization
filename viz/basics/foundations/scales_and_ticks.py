"""
Scales and ticks -- the axis is an argument, not furniture.

What it shows:
    * a log scale turns "I can only see the biggest one" into a readable chart
    * log is for ratios; it is the wrong tool for data containing zero
    * tick formatting: thousands separators, percentages, currency
    * date axes, which matplotlib handles specially

Run it:
    python viz/basics/foundations/scales_and_ticks.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, temperatures                # noqa: E402

# --- 1. when a linear axis hides everything --------------------------------
countries = ["Tuvalu", "Iceland", "Ireland", "Poland", "Brazil", "USA", "China"]
gdp = [0.06, 30, 550, 810, 2170, 27360, 17790]      # billions USD

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.barh(countries, gdp, color="#4C72B0")
left.set_title("Linear: five of the seven bars are invisible")
left.set_xlabel("GDP ($bn)")

right.barh(countries, gdp, color="#4C72B0")
right.set_xscale("log")
right.set_title("Log: every value readable, but read it as RATIOS")
right.set_xlabel("GDP ($bn), log scale")

fig.suptitle("Log scale: each step is a multiple, not an addition", fontsize=11)
fig.tight_layout()
save(fig, __file__, "log-scale")

# --- 2. what a log scale costs you -----------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

x = np.arange(1, 25)
doubling = 2.0 ** (x / 3)

left.plot(x, doubling, "-o", color="#C44E52", markersize=3)
left.set_title("Linear: 'it exploded at the end'")

right.plot(x, doubling, "-o", color="#C44E52", markersize=3)
right.set_yscale("log")
right.set_title("Log: a straight line = a CONSTANT growth rate")

fig.suptitle("Same data. The log version reveals that nothing changed.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "log-reveals-rate")

# --- 3. tick formatting ----------------------------------------------------
revenue = np.array([1_250_000, 2_100_000, 3_400_000, 4_050_000, 5_600_000])
quarters = ["Q1", "Q2", "Q3", "Q4", "Q5"]

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

left.bar(quarters, revenue, color="#4C72B0")
left.set_title("Default: what am I looking at? 1e6?")

right.bar(quarters, revenue, color="#4C72B0")
# A formatter is a function matplotlib calls for each tick value.
right.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"${v/1e6:.1f}M"))
right.set_title("Formatted: units on the ticks, not in a footnote")

fig.tight_layout()
save(fig, __file__, "tick-format")

# --- 4. date axes ----------------------------------------------------------
import matplotlib.dates as mdates                    # noqa: E402

temps = temperatures()

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

left.plot(temps["date"], temps["temp_c"], lw=0.8, color="#4C72B0")
left.set_title("Default date ticks")
left.tick_params(axis="x", rotation=45)

right.plot(temps["date"], temps["temp_c"], lw=0.8, color="#4C72B0")
right.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
right.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
right.set_title("Locator picks WHERE, formatter picks HOW it reads")

for ax in (left, right):
    ax.set_ylabel("temp (C)")

fig.tight_layout()
save(fig, __file__, "date-axis")

print("""
  The axis is part of the argument:
    huge range, all positive   -> log scale (ratios, never zero)
    straight line on a log y   -> constant growth rate
    big numbers                -> format the ticks, do not make people count zeros
    dates                      -> Locator = where, Formatter = how it reads
""")
