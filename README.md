# ApplyThon Trading Research

Beginner-friendly trading backtests with realistic costs — part of my ApplyThon research project on LLM trading agents and AI herding.

## About me
I am a B.Tech CSE (AI specialization) student researching AI in finance. I have authored two review papers:

1. **"From Language to Leverage?"** — a critical review of 21 studies on LLM-based trading agents, proposing an 8-stage evaluation protocol (point-in-time data, chronological validation, execution costs, risk reporting, ablations, reproducibility).
2. **"One Market, One Mind?"** — a research framework for measuring AI herding, position crowding, and loss amplification when many LLM agents share a model and information feed (2×2 factorial design, 4 measurement layers, 4 testable hypotheses).

## What this repo contains
My first hands-on backtest, built as a complete beginner:

- `starter_backtest_nolibs.py` — a simple momentum rule (buy after 5-day price rise, sell after fall) tested on 1 year of Apple (AAPL) data, **with realistic 0.1% transaction fees**
- `apple_stock_1year.csv` — the dataset (from Yahoo Finance)
- `my_first_backtest.svg` — result chart

## Key finding (an honest one)
The momentum strategy returned ~13%, while simply buying and holding returned ~33%.
The simple strategy **underperformed** — which is exactly the evidence gap my first paper documents:
many published LLM trading systems claim profits while ignoring realistic costs,
strong baselines, and reproducibility. I am learning to evaluate trading systems the honest way.

## What I plan to build during ApplyThon
Execute Stage 1 of my herding framework: run multiple LLM agents on identical
market data, measure signal agreement (Hypothesis H1), and publish a reproducible
mini-experiment with full code, prompts, and costs.
