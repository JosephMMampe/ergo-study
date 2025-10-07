# referflow — AI-powered referral content starter

Generate a small static site (index + product articles) from a CSV of items with affiliate URLs.

## Quickstart
```bash
python -m referflow.cli init          # writes sample CSV and config
python -m referflow.cli build \
  --config config.yaml \
  --csv products.csv \
  --out site
python -m http.server -d site 8080
