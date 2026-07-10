# IncuBot 2.0 — National Startup Incubator & Cross-State Fiscal Arbitrage

> **AI-powered startup policy intelligence platform** — IBM Watsonx Orchestrate live chat
> · DPIIT National Report 2026 anchored · Python Flask 3 · Bootstrap 5 Glassmorphism UI

---

## Features

| Feature | Details |
|---------|---------|
| **Watsonx Orchestrate Chat** | Live embedded web-chat client via `wxoLoader.js` (right-side panel) |
| **Fiscal Arbitrage Matrix** | Cross-state grant-stack & composite score comparison (8 states) |
| **9-Pillar Business Model Canvas** | Interactive visual grid layout |
| **MVP Technical Stack** | Layered architecture map (Frontend → DevOps) |
| **6-Month Roadmap** | Phased milestone timeline to GA launch |
| **Policy Anchor Strip** | SISFS caps, FFS corpus, 80-IAC holiday from DPIIT report |
| **Health Status Indicator** | `● AI: Connected` badge when `FLASK_SECRET_KEY` is set |
| **Dark / Light Mode** | One-click theme toggle, persisted in `localStorage` |
| **Glassmorphism UI** | Bootstrap 5, frosted glass cards, fade-in scroll animations |
| **Mobile-first** | Responsive breakpoints down to 320 px |

---

## Architecture Note

The conversation layer is powered **entirely via a frontend web-script handshake** linked to
IBM Watsonx Orchestrate. The `#root` element in `templates/index.html` mounts the official
`wxoLoader.js` widget directly — **no `WATSONX_PROJECT_ID` is required or checked on the backend.**

```
Browser  ──►  Flask (app.py)  ──►  templates/index.html
                                         │
                              window.wxOConfiguration
                                         │
                              wxoLoader.js  ──►  IBM Watsonx Orchestrate
                                                  (us-south.watson-orchestrate.cloud.ibm.com)
```

---

## Prerequisites

| Requirement | Minimum Version |
|-------------|----------------|
| Python | 3.10+ |
| pip | 23+ |

---

## Quick Start

### 1. Clone / download

```bash
git clone <your-repo-url>
cd incubot2
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Activate — macOS / Linux
source .venv/bin/activate

# Activate — Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the secret key

```bash
cp .env.example .env
```

Open `.env` and set at minimum:

```dotenv
# Required — set any strong random string; presence enables the "● AI: Connected" badge
FLASK_SECRET_KEY=<random-32-char-string>

# Optional
FLASK_PORT=5000
FLASK_DEBUG=true
```

> **Tip:** The full dashboard — including the Watsonx Orchestrate chat panel — renders with
> only `FLASK_SECRET_KEY` set. No IBM Cloud API key or project ID is needed.

### 5. Run the development server

```bash
python app.py
```

Navigate to **http://localhost:5000**

---

## Production Deployment (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

Or deploy to **IBM Code Engine** (recommended):

```bash
ibmcloud ce project select --name incubot2
ibmcloud ce app create \
  --name incubot2 \
  --image icr.io/<namespace>/incubot2:latest \
  --env-from-secret incubot2-secrets \
  --port 5000
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Dashboard HTML |
| `GET`  | `/api/health` | Service health + AI connection status |
| `GET`  | `/api/arbitrage` | Full cross-state matrix JSON |
| `GET`  | `/api/kpis` | KPI card data |
| `GET`  | `/api/roadmap` | 6-month roadmap |
| `GET`  | `/api/pillars` | 9-pillar canvas data |
| `GET`  | `/api/stack` | MVP tech stack |

---

## AGENT_INSTRUCTIONS Summary

The `app.py` file contains a full `AGENT_INSTRUCTIONS` block (top-of-file docstring) that
governs all AI reasoning, grounded in the **DPIIT "National-Report-15-01-26.pdf"**:

| Parameter | Value |
|-----------|-------|
| SISFS PoC Grant Cap | ₹ 20 Lakh (non-dilutive) |
| SISFS Prototype Cap | ₹ 50 Lakh |
| SISFS FFS / Market Entry Cap | ₹ 75 Lakh |
| FFS Corpus (SIDBI) | ₹ 10,000 Cr; sub-fund tickets ₹ 25–500 Cr |
| Tier-1 state grant co-commitment | ₹ 5 Cr per incubatee cycle |
| Tier-2 state grant co-commitment | ₹ 2 Cr; 30-day single-window clearance |
| Special category top-up | +25 % (NE, J&K, Ladakh, Andaman) |
| 80-IAC Tax Holiday | 3 of 10 consecutive years |

### Single-Window Portal Map

| State | Portal |
|-------|--------|
| Karnataka | Udyog Mitra → invest.karnataka.gov.in |
| Maharashtra | InvestMaharashtra → invest.maharashtra.gov.in |
| Telangana | TS-iPASS → ipass.telangana.gov.in |
| Gujarat | iNDEXTb SWAS → ic.gujarat.gov.in |
| Uttar Pradesh | Nivesh Mitra → niveshmitra.up.nic.in |
| Default | Startup India Hub → startupindia.gov.in |

---

## Project Structure

```
incubot2/
├── app.py                  # Flask app + AGENT_INSTRUCTIONS + API routes
├── templates/
│   └── index.html          # Full dashboard UI (Bootstrap 5, glassmorphism, wxO widget)
├── static/
│   ├── css/                # Optional override CSS
│   └── js/                 # Optional custom JS
├── requirements.txt        # Python dependencies (flask, python-dotenv, gunicorn)
├── .env.example            # Credential template — copy to .env
├── .env                    # Local secrets — NEVER commit
└── README.md               # This file
```

---

## Security Notes

- `.env` is **never** committed (add to `.gitignore`)
- `FLASK_SECRET_KEY` loaded via `python-dotenv` — not hardcoded
- Watsonx Orchestrate credentials are embedded only in the **client-side** widget config
  (orchestration IDs are non-secret deployment identifiers, not API keys)
- For production, use **IBM Secrets Manager** or **Code Engine secrets** instead of `.env`

---

*Made with IBM Bob*
