"""
LESSON 1 — STEP 1: Download BTC/USDT 4-hour candles from Binance (public, no account needed).

What this script does, in plain words:
  1. Asks Binance's website for historical 4-hour candles (about 2.5+ years).
  2. Cleans them up (removes duplicates, sorts oldest to newest).
  3. Saves them into data/btcusdt_4h.csv so every later lesson reuses them.
  4. Prints a short report so you can check it worked.

How to run it (from the crypto-lab folder):
  python scripts/01_download_data.py
"""

import csv
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------- SETTINGS (don't change these today) ----------------
SYMBOL      = "BTCUSDT"    # the pair we study. Rule 2: ONE pair only.
INTERVAL    = "4h"         # 4-hour candles. Rule 3: ONE timeframe only.
LIMIT       = 1000         # max candles Binance hands out per request (their cap)
MAX_PAGES   = 14           # batches to fetch (14 x 1000 = ~6.5 years of history)
START_DATE  = "2021-01-01" # collect candles from this date (UTC) onward
                           # 2021 = mania + top, 2022 = bear (Luna, FTX),
                           # 2023 = recovery, 2024-2026 = current cycle
INTERVAL_MS = 4 * 60 * 60 * 1000   # one 4-hour candle = 14,400,000 milliseconds

# Save next to the project folder no matter where you run the script from:
OUT_FILE = Path(__file__).resolve().parent.parent / "data" / "btcusdt_4h.csv"

# Binance runs several copies of the same data. Professionals never depend on
# one door, so we try them in order until one answers:
HOSTS = [
    "https://api.binance.com",
    "https://data-api.binance.vision",   # Binance's official public-data mirror
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com",
    "https://api.binance.us",            # the US cousin; near-identical data
]
BASE = HOSTS[0]   # replaced by the first host that answers (set in probe_hosts)


# ---------------- STEP A: one HTTP call to the chosen host ----------------
def call_api(path, timeout=20):
    """Small helper: one GET request, answer decoded as Python data."""
    request = urllib.request.Request(BASE + path, headers={"User-Agent": "crypto-lab/lesson1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode())


def probe_hosts():
    """Knock on every Binance door until one opens. Servers fall over all the
    time - a data pipeline that assumes 'the server will always be there'
    is a pipeline that will waste YOUR evening one day."""
    global BASE
    for i, host in enumerate(HOSTS, 1):
        BASE = host
        try:
            call_api("/api/v3/ping", timeout=10)
            print(f"Data host in use: {host} ({i}/{len(HOSTS)})")
            return
        except Exception:
            print(f"  host {i}/{len(HOSTS)} not answering -> trying next...")
    raise SystemExit(
        "Every Binance data host refused to answer. Either your internet is "
        "down or security software is blocking them. Check and re-run later."
    )


def fetch_page(start_ms, attempts=4):
    """One request = up to `LIMIT` candles starting at time start_ms.

    Networks and APIs hiccup, so we retry a few times with growing pauses.
    Real data pipelines ALWAYS do this - a script that dies on the first
    dropped connection is a toy.
    """
    path = f"/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&startTime={start_ms}&limit={LIMIT}"
    for attempt in range(1, attempts + 1):
        try:
            return call_api(path)
        except (urllib.error.URLError, OSError) as problem:
            if attempt == attempts:
                raise   # out of patience - let the real error show
            wait = attempt * 2          # wait 2s, then 4s, then 6s...
            print(f"  Connection hiccup ({problem.__class__.__name__}). "
                  f"Waiting {wait}s, retry {attempt + 1}/{attempts}...")
            time.sleep(wait)


def fmt(ms):
    """Turn a Unix timestamp (milliseconds) into a readable UTC date."""
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def main():
    start_ms = int(
        datetime.strptime(START_DATE, "%Y-%m-%d")
        .replace(tzinfo=timezone.utc)
        .timestamp() * 1000
    )
    raw_rows = []

    # ---------------- STEP B0: pick a data host that actually answers -------
    probe_hosts()

    # ---------------- STEP B: fetch everything, page by page ----------------
    for page in range(1, MAX_PAGES + 1):
        rows = fetch_page(start_ms)
        if not rows:
            print(f"Page {page}: nothing more to fetch. We have all the history.")
            break
        raw_rows.extend(rows)
        print(f"Page {page}: got {len(rows)} candles ({fmt(rows[0][0])} -> {fmt(rows[-1][0])})")
        if len(rows) < LIMIT:          # fewer than the max means we reached today
            break
        start_ms = rows[-1][0] + INTERVAL_MS
        time.sleep(0.3)                # short pause between requests (good manners)

    if not raw_rows:
        print("No data came back. Check your internet connection, then try again.")
        return

    # ---------------- STEP C: clean up ----------------
    # Each raw row from Binance looks like:
    # [open_time, open, high, low, close, volume, close_time, ..., trades, ...]
    seen, clean = set(), []
    for r in sorted(raw_rows, key=lambda r: int(r[0])):
        if r[0] in seen:               # skip duplicates
            continue
        seen.add(r[0])
        clean.append({
            "time_utc": datetime.fromtimestamp(r[0] / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
            "open":  r[1],
            "high":  r[2],
            "low":   r[3],
            "close": r[4],
            "volume": r[5],
            "trades": r[8],
        })

    # ---------------- STEP D: save to CSV + print a report ----------------
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)   # make the data/ folder if missing
    with open(OUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(clean[0].keys()))
        writer.writeheader()
        writer.writerows(clean)

    closes = [float(row["close"]) for row in clean]
    print("-" * 60)
    print(f"Saved {len(clean)} candles to {OUT_FILE.name}")
    print(f"Range: {clean[0]['time_utc']} -> {clean[-1]['time_utc']} (UTC)")
    print(f"BTC price then: ${closes[0]:,.0f} | BTC price now: ${closes[-1]:,.0f}")
    print("Lesson 1, Step 1 complete. Open the CSV in a spreadsheet and look at it.")


# This final line means: "run the main() function when executed as a script."
if __name__ == "__main__":
    main()
