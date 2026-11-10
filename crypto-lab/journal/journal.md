# Trading Journal

> Rule 5 of the contract: no idea and no trade goes unwritten. A trade you can't
> explain in one sentence is a coin flip wearing a costume.
>
> One idea per entry. Be blunt. This journal is for you, not to look smart.

---

## Template (copy this block for every new idea or trade)

```
### 2026-__-__ — Idea #___
**Pair / timeframe:** BTCUSDT / 4H
**One-sentence hypothesis:**
(e.g. "When BTC 4H price pulls back to EMA21 while RSI > 50, the next candle
closes higher more often than random.")
**Why I believe it:**
**How I will test it:**
**What would prove me wrong:**
**Status:** idea | backtesting | paper | live | killed
**Result / lesson (fill in after test):**
```

---

## Ideas log

### 2026-11-04 — Idea #001
**Pair / timeframe:** BTCUSDT / 4H
**One-sentence hypothesis:** _(fill this in — this is your homework)_
**Why I believe it:** _(to be filled)_
**How I will test it:** backbone test from Lesson 3: EMA 9/21 cross, fees included
**What would prove me wrong:** losing money after fees on out-of-sample data
**Status:** idea
**Result / lesson:** _(to be filled)_

---

## Lab notes (decisions that outlive a single week)

**2026-11-04 — Data policy.** History now starts at 2021-01-01 (not 2024).
Reason: 2021-2022 contains the mania, the top, Luna, and FTX — a full bear
market. A strategy never tested on a bear is a fantasy. Two rules attached:
(1) parameters get fit on *recent* data; older history is for stress-testing
survival, (2) we do not reach further back than 2021 — the market's
microstructure gets less and less comparable the deeper you dig.

**2026-11-04 — Engineering note.** The data downloader now retries failed
requests automatically (4 tries, growing pauses). Lesson: networks fail;
professionals build for failure, amateurs hope for luck.

---

## Weekly review (every week, same day, 1 hour)

- What did I work on this week?
- What did the market do, and did my idea hold up against it?
- Biggest mistake? (Not knowing is NOT an acceptable answer — find it in the data.)
- One thing to do differently next week.
