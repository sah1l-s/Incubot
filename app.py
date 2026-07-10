"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              IncuBot 2.0 — National Startup Incubator Dashboard              ║
║          Cross-State Fiscal Arbitrage + IBM Watsonx Orchestrate              ║
╚══════════════════════════════════════════════════════════════════════════════╝

AGENT_INSTRUCTIONS
──────────────────
This backend anchors ALL operational reasoning to the parameters defined in
the DPIIT "National-Report-15-01-26.pdf" (Startup India Annual Report 2026).

The conversation layer is powered entirely via a frontend web-script handshake
directly linked to IBM Watsonx Orchestrate — NO WATSONX_PROJECT_ID is required
or checked on the backend. The '#root' element in index.html loads the official
IBM wxoLoader.js widget which handles all agent session management client-side.

KEY POLICY ANCHORS THE AI AGENT MUST OBSERVE
─────────────────────────────────────────────

1. SISFS SEED-FUND CAPS  (Startup India Seed Fund Scheme)
   ┌──────────────────────────────────────────────────────────┐
   │  Grant / PoC Validation   :  up to ₹ 20 lakh (non-dilut)│
   │  Prototype Development    :  up to ₹ 50 lakh            │
   │  Market Entry Debt / Conv.:  up to ₹ 75 lakh (FFS cap)  │
   └──────────────────────────────────────────────────────────┘

2. FFS  (Fund of Funds for Startups) — SEBI-AIF compliant
   - SIDBI manages INR 10,000 Cr corpus; sub-fund tickets ₹ 25–500 Cr.
   - State co-investment multiplier must not exceed 2× centre corpus.

3. STATE-LEVEL FUNDING BOUNDARIES  (DPIIT Table 7, Annex III)
   - Tier-1 States  (Karnataka, Maharashtra, Kerala, TN):
       Max state-side grant co-commitment = ₹ 5 Cr per incubatee cycle.
   - Tier-2 States  (UP, Rajasthan, MP, Haryana):
       Max = ₹ 2 Cr; single-window clearance via Nivesh Mitra / Invest
       Rajasthan portal mandated within 30 business days.
   - Emerging States  (NE, J&K, Ladakh, Andaman):
       Max = ₹ 1 Cr; DPIIT special category boost of +25 % grant top-up.

4. LOCAL ADMINISTRATIVE SINGLE-WINDOW PATHS
   - Karnataka   → Udyog Mitra      (invest.karnataka.gov.in)
   - Maharashtra → InvestMaharashtra (invest.maharashtra.gov.in)
   - Telangana   → T-Hub / TS-iPASS  (ipass.telangana.gov.in)
   - Gujarat     → iNDEXTb SWAS      (ic.gujarat.gov.in)
   - UP          → Nivesh Mitra      (niveshmitra.up.nic.in)
   - Default     → Startup India Hub  (startupindia.gov.in)
   All paths must be surfaced in AI suggestions before any cross-state
   arbitrage recommendation is finalised.

5. ARBITRAGE EVALUATION LOGIC
   The agent MUST compare at minimum:
   (a) Effective grant stack  (state + centre)
   (b) Tax holiday duration   (DPIIT Section 80-IAC: 3 of 10 years)
   (c) Real-estate incubation space subsidy  (sq-ft cost delta)
   (d) Talent pipeline density  (engineering graduate output per state)
   before surfacing a fiscal arbitrage score for any state pair.

6. PROHIBITED ACTIONS
   - Agent must NOT recommend non-DPIIT-recognised incubators.
   - Agent must NOT quote seed amounts above SISFS statutory caps.
   - Agent must NOT bypass single-window administrative paths.
"""

import os
import logging
from datetime import datetime

from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

# ─── Environment ─────────────────────────────────────────────────────────────
load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-production")
FLASK_PORT       = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG      = os.getenv("FLASK_DEBUG", "true").lower() == "true"

# NOTE: WATSONX_PROJECT_ID is intentionally NOT loaded or validated here.
# The Watsonx Orchestrate conversation is handled entirely by the frontend
# IBM wxoLoader.js widget via the window.wxOConfiguration handshake.

# ─── Flask app ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ─── Dashboard data  ──────────────────────────────────────────────────────────

STATE_MATRIX = [
    {
        "state": "Karnataka",       "tier": "Top Performer",
        "grant_stack_cr": 5.0,      "tax_holiday_yrs": 3,
        "incubators": 185,          "seed_disbursed_cr": 312,
        "single_window": "Udyog Mitra",
        "portal": "invest.karnataka.gov.in",
        "arbitrage_score": 94,
    },
    {
        "state": "Maharashtra",     "tier": "Top Performer",
        "grant_stack_cr": 5.0,      "tax_holiday_yrs": 3,
        "incubators": 210,          "seed_disbursed_cr": 290,
        "single_window": "InvestMaharashtra",
        "portal": "invest.maharashtra.gov.in",
        "arbitrage_score": 91,
    },
    {
        "state": "Telangana",       "tier": "Top Performer",
        "grant_stack_cr": 4.5,      "tax_holiday_yrs": 3,
        "incubators": 96,           "seed_disbursed_cr": 178,
        "single_window": "TS-iPASS",
        "portal": "ipass.telangana.gov.in",
        "arbitrage_score": 88,
    },
    {
        "state": "Tamil Nadu",      "tier": "Top Performer",
        "grant_stack_cr": 4.0,      "tax_holiday_yrs": 3,
        "incubators": 112,          "seed_disbursed_cr": 155,
        "single_window": "Guidance TN",
        "portal": "investtn.in",
        "arbitrage_score": 85,
    },
    {
        "state": "Gujarat",         "tier": "Emerging",
        "grant_stack_cr": 2.5,      "tax_holiday_yrs": 3,
        "incubators": 74,           "seed_disbursed_cr": 89,
        "single_window": "iNDEXTb SWAS",
        "portal": "ic.gujarat.gov.in",
        "arbitrage_score": 75,
    },
    {
        "state": "Uttar Pradesh",   "tier": "Emerging",
        "grant_stack_cr": 2.0,      "tax_holiday_yrs": 3,
        "incubators": 62,           "seed_disbursed_cr": 74,
        "single_window": "Nivesh Mitra",
        "portal": "niveshmitra.up.nic.in",
        "arbitrage_score": 68,
    },
    {
        "state": "Rajasthan",       "tier": "Emerging",
        "grant_stack_cr": 2.0,      "tax_holiday_yrs": 3,
        "incubators": 48,           "seed_disbursed_cr": 53,
        "single_window": "Invest Rajasthan",
        "portal": "invest.rajasthan.gov.in",
        "arbitrage_score": 62,
    },
    {
        "state": "Meghalaya",       "tier": "Special Category",
        "grant_stack_cr": 1.25,     "tax_holiday_yrs": 3,
        "incubators": 14,           "seed_disbursed_cr": 12,
        "single_window": "StartupMeghalaya",
        "portal": "startups.meghalaya.gov.in",
        "arbitrage_score": 55,
    },
]

NINE_PILLARS = [
    {"id": 1, "name": "Value Proposition",  "icon": "💡", "desc": "AI-driven fiscal gap analysis for founders navigating multi-state grant stacks."},
    {"id": 2, "name": "Customer Segments",  "icon": "👥", "desc": "Early-stage DPIIT-recognised startups, incubation managers, state nodal officers."},
    {"id": 3, "name": "Channels",           "icon": "📡", "desc": "SaaS web dashboard, WhatsApp Business API nudges, government portal API hooks."},
    {"id": 4, "name": "Customer Relations", "icon": "🤝", "desc": "Watsonx Orchestrate AI concierge, 1:1 mentor matching, cohort peer circles."},
    {"id": 5, "name": "Revenue Streams",    "icon": "💰", "desc": "Subscription SaaS tiers, success-fee on grant disbursement, data-as-a-service."},
    {"id": 6, "name": "Key Resources",      "icon": "🏛️",  "desc": "IBM Watsonx Granite LLMs, DPIIT policy corpus, state fiscal database, partner APIs."},
    {"id": 7, "name": "Key Activities",     "icon": "⚙️",  "desc": "Policy arbitrage scoring, automated compliance checks, real-time grant tracking."},
    {"id": 8, "name": "Key Partnerships",   "icon": "🔗", "desc": "SIDBI, DPIIT nodal cells, NASSCOM 10k, state ATL/TBI incubator networks."},
    {"id": 9, "name": "Cost Structure",     "icon": "📊", "desc": "IBM Cloud compute, data licensing, BD & regulatory affairs team, compliance audits."},
]

MVP_STACK = {
    "frontend":  ["React 18 + Vite", "Tailwind CSS 3", "Recharts / Nivo", "IBM Carbon Design"],
    "backend":   ["Python Flask / FastAPI", "Celery + Redis", "PostgreSQL 16", "Alembic migrations"],
    "ai_layer":  ["IBM Watsonx.ai Granite", "LangChain 0.3", "pgvector RAG store", "Watsonx Orchestrate"],
    "infra":     ["IBM Code Engine", "IBM Cloud Object Storage", "API Connect", "Secrets Manager"],
    "devops":    ["GitHub Actions CI/CD", "Terraform IaC", "Sentry monitoring", "Datadog APM"],
}

ROADMAP = [
    {"month": "M1–M2", "phase": "Foundation", "milestone": "Core Flask API, DPIIT corpus ingestion, Granite RAG baseline, Design system"},
    {"month": "M3",    "phase": "Alpha",       "milestone": "State matrix scoring engine, SISFS compliance checker, Auth & multi-tenancy"},
    {"month": "M4",    "phase": "Beta",        "milestone": "Watsonx Orchestrate chat integration, grant-tracking pipeline, mobile-first UI"},
    {"month": "M5",    "phase": "Pilot",       "milestone": "Onboard 3 state nodal officers, WhatsApp nudge engine, analytics dashboards"},
    {"month": "M6",    "phase": "GA Launch",   "milestone": "Public SaaS launch, SIDBI partnership MoU, Series-A pitch deck generation"},
]

KPI_CARDS = [
    {"label": "DPIIT Recognised Startups",   "value": "1,47,362", "delta": "+22 % YoY",     "trend": "up"},
    {"label": "States with Active SISFS",     "value": "31",       "delta": "4 new in FY26",  "trend": "up"},
    {"label": "Total Seed Disbursed (₹ Cr)",  "value": "2,116",    "delta": "+18 % FY26",     "trend": "up"},
    {"label": "FFS Corpus Deployed (₹ Cr)",   "value": "7,850",    "delta": "of ₹10,000 Cr",  "trend": "neutral"},
    {"label": "Avg Arbitrage Score Delta",    "value": "26 pts",   "delta": "Top vs Emerging", "trend": "up"},
    {"label": "80-IAC Tax Beneficiaries",     "value": "4,211",    "delta": "+31 % YoY",      "trend": "up"},
]

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    # AI is "connected" whenever a non-default Flask secret key is configured
    ai_connected = FLASK_SECRET_KEY != "dev-secret-change-in-production"
    return render_template(
        "index.html",
        state_matrix=STATE_MATRIX,
        nine_pillars=NINE_PILLARS,
        mvp_stack=MVP_STACK,
        roadmap=ROADMAP,
        kpi_cards=KPI_CARDS,
        ai_connected=ai_connected,
        current_year=datetime.now().year,
    )


@app.route("/api/health")
def health():
    ai_connected = FLASK_SECRET_KEY != "dev-secret-change-in-production"
    return jsonify({
        "status":       "ok",
        "service":      "IncuBot 2.0",
        "ai_connected": ai_connected,
        "timestamp":    datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/arbitrage")
def arbitrage_matrix():
    return jsonify({"states": STATE_MATRIX})


@app.route("/api/kpis")
def kpis():
    return jsonify({"kpis": KPI_CARDS})


@app.route("/api/roadmap")
def get_roadmap():
    return jsonify({"roadmap": ROADMAP})


@app.route("/api/pillars")
def pillars():
    return jsonify({"pillars": NINE_PILLARS})


@app.route("/api/stack")
def stack():
    return jsonify({"stack": MVP_STACK})


# ─── Entrypoint ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting IncuBot 2.0 on port %s (debug=%s)", FLASK_PORT, FLASK_DEBUG)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
