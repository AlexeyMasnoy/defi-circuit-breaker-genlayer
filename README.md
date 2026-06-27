# genlayer-defi-circuit-breaker

> An Intelligent Contract that safeguards DeFi protocols by monitoring real-time news and social sentiment using AI. Automatically triggers on-chain circuit breakers to protect assets when exploits or extreme market FUD are detected — no human intervention needed.

---

## Overview

DeFi protocols are highly vulnerable to "black swan" events and sudden exploits. This contract acts as an automated risk management layer. Instead of waiting for manual governance votes, the contract independently fetches real-time news via web requests, uses AI to analyze the sentiment, and if an exploit or severe FUD is detected, it switches the protocol to a `paused` state immediately.

This is the automated safety oracle rebuilt as a full adjudication contract: live data fetch, AI sentiment judgment, and enforced on-chain circuit breaking.

---

## Use Cases

- **Exploit Protection** — automatically pauses withdrawals if news of a protocol hack hits the web
- **FUD Mitigation** — prevents panic-selling or liquidity drain during extreme market sentiment shifts
- **Oracle Validation** — degrades trust in external data providers when reports of manipulation appear
- **Risk Management** — gives infrastructure teams a reliable control layer for defensive protocol actions

---

## Repository Structure

genlayer-defi-circuit-breaker/
├── circuit_breaker.py   ← main contract (verified on Studio)
├── LICENSE
└── README.md

## Methods

### Write Methods

| Method | Parameters | Description |
|---|---|---|
| `run_health_check` | `token: str`, `news_data: str` | Fetches/Receives data, triggers AI consensus, updates pause status. |

### Read Methods

| Method | Parameters | Description |
|---|---|---|
| `get_status` | — | Returns current state (True if paused, False if safe). |
| `last_analysis_reason` | — | Returns the rationale behind the last AI decision. |

---

## Risk Indicators

| Signal | AI Interpretation | Action |
|---|---|---|
| "Hack / Exploit" | Critical | Pause Protocol |
| "Security Vulnerability" | High | Partial Limit |
| "Market FUD" | Moderate | Monitor |
| "Normal Trading" | Safe | Allow |

---

## Data Source

**News Aggregators** (e.g., CryptoPanic, Binance News, or X). The contract is designed to ingest text-based news data directly from the web, allowing GenLayer validators to perform decentralized sentiment analysis on the raw headlines.

---

## Deploying

1. Open [studio.genlayer.com](https://studio.genlayer.com)
2. Paste `circuit_breaker.py` into the editor
3. Click **Deploy new instance**
4. Wait for FINALIZED

---

## Quick Test


```
run_health_check(
token="ETH",
news_data="Critical security vulnerability discovered in ETH bridge, funds at risk."
)

Check if the circuit breaker was triggered
get_status()

```

## Consensus Safety

News sentiment is judged using `gl.eq_principle`. Validators fetch news independently or verify the provided input. The contract uses AI to ensure consensus on the *interpretation* of the news (e.g., "Is this FUD or a real hack?"). This protects the protocol from being manipulated by biased or incorrect web-data sources.

---

## Verified On-Chain

Deployed and tested on GenLayer Studio (studionet, GenVM v0.2.16). News analysis reached consensus, contract state successfully toggled to `paused` upon detection of high-risk sentiment, and access to dependent functions was restricted.

---

## License

MIT — see [LICENSE](./LICENSE)
