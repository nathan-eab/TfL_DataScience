# London Bus Route Efficiency Analytics

An interactive dashboard that measures how *regular* (not just "on time" — TfL doesn't publish bus schedules) London bus routes really are, using live data from the **TfL Unified API**. It tracks headway consistency over time and explores whether route reliability correlates with borough-level socioeconomic and infrastructure factors.

> TfL doesn't expose a static bus timetable or live vehicle GPS to third parties, and bus operator/vehicle-model data isn't available via the API either. So instead of "actual vs scheduled," this project measures **headway regularity** — how consistent the gaps between buses are — which is closer to the metric TfL itself uses operationally (Excess Wait Time).

## What it does

- Continuously polls live bus arrival predictions from the TfL Unified API and stores them over time (there's no historical endpoint, so this project *generates* its own time-series dataset).
- Computes a **route efficiency score** per line/stop using the coefficient of variation (SD ÷ mean) of headways — normalised so high-frequency and low-frequency routes are comparable.
- Tags every stop with its **London borough** via a spatial join against borough boundary data.
- Runs a **Pearson correlation (PMCC)** between route efficiency and borough-level factors (deprivation index, population density, traffic flow, and more) to explore whether *where* a route runs predicts *how reliable* it is — with proper caveats around sample size and correlation-vs-causation.
- Presents everything through an interactive Flask + Tailwind dashboard with toggleable filters (borough / route) and Chart.js visualisations, plus a dedicated correlations view.

## Tech stack

- **Backend**: Python, Flask, SQLAlchemy, APScheduler (background polling)
- **Database**: SQLite (dev) — swappable to PostgreSQL
- **Data analysis**: pandas, scipy (`pearsonr`)
- **Geo**: Shapely / GeoPandas (borough spatial join)
- **Frontend**: Tailwind CSS, Chart.js, vanilla JS
- **Data sources**: [TfL Unified API](https://api.tfl.gov.uk), [London Datastore](https://data.london.gov.uk) (borough factors)

## Project status

🚧 Work in progress — built in public, phase by phase. See [Roadmap](#roadmap) below.

## Getting started

### Prerequisites
- Python 3.11+
- A free TfL API key from the [TfL API Portal](https://api-portal.tfl.gov.uk)

### Setup
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env       # then add your TfL app_id / app_key
```

### Running locally
```bash
# Seed reference data (lines, stops, boroughs) — run once
python scripts/seed_lines.py

# Start the live data poller (separate process, leave running)
python poller.py

# In another terminal, start the web app
flask run
```
Visit `http://localhost:5000`.

> Note: this app needs the poller running continuously to build up meaningful data — efficiency stats won't be interesting until it's been collecting for at least a few days.

## Project structure
```
app/
  models.py          # SQLAlchemy models
  tfl_client.py       # TfL API wrapper
  poller.py           # background data collection job
  routes/             # Flask views + JSON API
  templates/
  static/
scripts/
  seed_lines.py        # one-off DB seeding
  borough_lookup.py    # spatial join: stops -> boroughs
.env.example
requirements.txt
```

## Roadmap
- [ ] Phase 1 — Live data fetch working
- [ ] Phase 2 — Persistence (DB + poller)
- [ ] Phase 3 — Borough enrichment + factor data
- [ ] Phase 4 — Headway/efficiency aggregation
- [ ] Phase 4b — PMCC correlation analysis
- [ ] Phase 5 — API + dashboard frontend
- [ ] Phase 6 — Deploy + polish

## Methodology notes

Full reasoning behind the metric choices, data limitations, and the correlation methodology (including statistical caveats) is documented in [`docs/methodology.md`](docs/methodology.md).

## Data sources & attribution

- Bus arrival data: Transport for London ([TfL Open Data licence](https://tfl.gov.uk/info-for/open-data-users/))
- Borough boundaries & socioeconomic data: [London Datastore](https://data.london.gov.uk), Greater London Authority / ONS
