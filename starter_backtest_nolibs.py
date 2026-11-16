"""
Starter backtest - standard library only (no pandas / matplotlib).
Rule-based momentum strategy vs Buy-and-Hold, WITH transaction costs.
Run:  python starter_backtest_nolibs.py apple_stock_1year.csv
Output: printed results + my_first_backtest.svg (open it in a browser)
"""
import csv
import os
import sys
from datetime import datetime

# ---------- 1. Load data ----------
here = os.path.dirname(os.path.abspath(__file__))
csv_file = sys.argv[1] if len(sys.argv) > 1 else "apple_stock_1year.csv"
if not os.path.isabs(csv_file):
    csv_file = os.path.join(here, csv_file)   # look next to this script

rows = []
with open(csv_file, newline="") as f:
    for r in csv.DictReader(f):
        rows.append((datetime.strptime(r["Date"], "%Y-%m-%d"), float(r["Close"])))
rows.sort()
close = [c for _, c in rows]

START_CASH = 10000.0
FEE_PCT = 0.001          # 0.1% fee per trade
HISTORY = 5              # look back 5 days

# ---------- 2. Rule-based strategy ----------
cash = START_CASH
shares = 0.0
in_market = False
strategy_value = []

for i in range(len(close)):
    if i >= HISTORY:
        momentum = close[i] - close[i - HISTORY]
        if momentum > 0 and not in_market:
            shares = cash * (1 - FEE_PCT) / close[i]
            cash = 0.0
            in_market = True
        elif momentum <= 0 and in_market:
            cash = shares * close[i] * (1 - FEE_PCT)
            shares = 0.0
            in_market = False
    strategy_value.append(cash + shares * close[i])

# ---------- 3. Buy-and-hold ----------
bh_shares = START_CASH * (1 - FEE_PCT) / close[0]
buyhold_value = [bh_shares * c for c in close]
price_scaled = [c / close[0] * START_CASH for c in close]

# ---------- 4. Report ----------
final_strategy = strategy_value[-1]
final_bh = buyhold_value[-1]
print("=" * 50)
print(f"Start:                         ${START_CASH:,.2f}")
print(f"Strategy (momentum with fees): ${final_strategy:,.2f}")
print(f"Buy & Hold (with fees):        ${final_bh:,.2f}")
print(f"Strategy return: {(final_strategy / START_CASH - 1) * 100:.1f}%")
print(f"Buy&Hold return: {(final_bh / START_CASH - 1) * 100:.1f}%")
print("=" * 50)

# ---------- 5. Plot (SVG, no libraries) ----------
W, H, PAD = 900, 450, 60
series = [
    (strategy_value, "#2a6fdb", "Rule-based strategy (fees included)", ""),
    (buyhold_value, "#e8851a", "Buy & Hold (fees included)", ""),
    (price_scaled, "#888888", "AAPL price (scaled)", "6,4"),
]
allv = [v for s, *_ in series for v in s]
lo, hi = min(allv), max(allv)
n = len(close)

def pt(i, v):
    x = PAD + i * (W - 2 * PAD) / (n - 1)
    y = H - PAD - (v - lo) * (H - 2 * PAD) / (hi - lo)
    return f"{x:.1f},{y:.1f}"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'font-family="Arial" font-size="12"><rect width="100%" height="100%" fill="white"/>',
       f'<text x="{W/2}" y="25" text-anchor="middle" font-size="16">'
       f'My first honest backtest - Day 1 of my ApplyThon project</text>']
for k in range(5):                                   # y-axis grid + labels
    v = lo + (hi - lo) * k / 4
    y = H - PAD - (v - lo) * (H - 2 * PAD) / (hi - lo)
    svg.append(f'<line x1="{PAD}" y1="{y:.1f}" x2="{W-PAD}" y2="{y:.1f}" stroke="#ddd"/>')
    svg.append(f'<text x="{PAD-6}" y="{y+4:.1f}" text-anchor="end">${v:,.0f}</text>')
svg.append(f'<text x="{PAD}" y="{H-PAD+20}">{rows[0][0]:%Y-%m-%d}</text>')
svg.append(f'<text x="{W-PAD}" y="{H-PAD+20}" text-anchor="end">{rows[-1][0]:%Y-%m-%d}</text>')
for k, (s, color, label, dash) in enumerate(series):
    pts = " ".join(pt(i, v) for i, v in enumerate(s))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"{d}/>')
    ly = H - 30 + k * 0
    svg.append(f'<rect x="{PAD + k*270}" y="{H-22}" width="14" height="4" fill="{color}"/>')
    svg.append(f'<text x="{PAD + k*270 + 20}" y="{H-16}">{label}</text>')
svg.append("</svg>")

out = os.path.join(here, "my_first_backtest.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print(f"Saved plot -> {out}")
