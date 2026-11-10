# CRYPTO LAB — the mentor's contract

This folder is your training ground. Every lesson lives here. Read this file whenever you feel lost.

## The contract (non-negotiable rules)

1. **No leverage. No futures. No margin.** Until 90+ days paper-trade profitable.
2. **One pair:** BTC/USDT. Nothing else.
3. **One timeframe:** 4H. Nothing else.
4. **One hypothesis at a time.** "Let me also add another indicator" = drift.
5. **Journal every idea and every trade** — in `journal/journal.md`.
6. **Fixed weekly review:** 1 hour, same day every week. This is where learning happens.
7. **Risk max 1% of account per trade.** Position size comes from the stop distance, never the reverse.
8. **Two losses in a day → done for the day.** Close the laptop.
9. **A backtest without fees and slippage is fiction.** Spot fees ≈ 0.1% per side.
10. **If a strategy only survives tiny parameter tweaks (RSI 14→15), it is noise. Kill it.**

## Folder map

```
crypto-lab/
├── README.md              ← you are here. The rules live here.
├── journal/journal.md     ← your trading journal (fill this in)
├── scripts/               ← the programs (lessons)
│   └── 01_download_data.py   ← Lesson 1: fetch BTC/USDT 4H history
└── data/                  ← downloaded candles (created automatically)
    └── btcusdt_4h.csv
```

## How to run Lesson 1

Open a terminal **inside this folder**, then:

```
python scripts\01_download_data.py
```

Expected output: ~6,000 candles downloaded (~2.5+ years) and saved to
`data/btcusdt_4h.csv`, plus a short report printed to the screen.

## The 12-week roadmap (20 hrs/week)

| Weeks | Focus | Output |
|---|---|---|
| 1–2 | Python basics + getting the data | Script that loads and plots 4H candles |
| 3–4 | First backtest: EMA 9/21 cross, fees included | Win rate, max drawdown, profit factor |
| 5–6 | RSI as a filter, VWAP as context; honest vs unfair testing | 2–3 tested hypotheses, one survivor |
| 7–8 | Sensibility check + walk-forward testing | One validated candidate + kill criteria |
| 9–12 | Paper trading (fake money, real markets) | 30+ journaled trades matching the backtest |

## Where we trade

Not yet. No account is needed for weeks 1–12 (data is public, paper trading is free).
Hyperliquid gets reviewed after 90 days of paper trading, not before.
