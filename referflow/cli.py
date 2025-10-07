from __future__ import annotations
import os
import json
import shutil
from typing import Optional
import typer  # Typer CLI: https://typer.tiangolo.com/tutorial/commands/
from rich import print
from .utils import assert_versions
from .config import load_config, AppCfg
from .data import load_products
from .render import build_site

app = typer.Typer(add_completion=False)

@app.command()
def init() -> None:
    """Write sample products.csv and config.yaml (idempotent)."""
    assert_versions()
    samples = "products.csv"
    cfg = "config.yaml"
    if not os.path.exists(samples):
        with open(samples, "w", encoding="utf-8") as f:
            f.write("""title,affiliate_url,price_eur,pros,cons,specs
"Inexpensive Laptop Stand","https://www.amazon.de/dp/B08XYZ?tag=YOURTAG-21",24.99,"Lightweight;Raises screen","Wobbles under heavy laptops","Height: up to 15cm; Material: Aluminum"
"Budget Desk Clamp Monitor Arm","https://www.bol.com/nl/p/12345/?referrer=affid",39.95,"Frees desk space;Cable routing","Limited tilt range","VESA: 75x75/100x100; Max load: 8kg"
"Simple Foot Rest","https://www.amazon.de/dp/B09ABC?tag=YOURTAG-21",17.50,"Soft;Non-slip","Small for tall users","Size: 40x20x10cm; Cover: Washable"
""")
        print("[green]Wrote products.csv[/green]")
    else:
        print("[yellow]products.csv already exists[/yellow]")
    if not os.path.exists(cfg):
        with open(cfg, "w", encoding="utf-8") as f:
            f.write("""site_name: "Ergo-Study Picks"
site_tagline: "Small-room ergonomics that actually help."
base_url: "http://localhost:8080"
dry_run: true
seed: 42
model:
  provider: "openai"
  model_name: "gpt-4o-mini"
  temperature: 0.2
  max_tokens: 800
theme:
  brand_color: "#0f766e"
  accent_color: "#f59e0b"
  font_stack: "system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial"
disclosure: "As an Amazon/Bol.com Associate I earn from qualifying purchases. No extra cost to you."
""")
        print("[green]Wrote config.yaml[/green]")
    else:
        print("[yellow]config.yaml already exists[/yellow]")

@app.command()
def build(
    config: str = typer.Option("config.yaml", "--config", help="Path to config.yaml"),
    csv: str = typer.Option("products.csv", "--csv", help="Path to products.csv"),
    out: str = typer.Option("site", "--out", help="Output directory"),
) -> None:
    """Build static site."""
    assert_versions()
    cfg: AppCfg = load_config(config)
    products = load_products(csv)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)
    build_site(cfg, products, out)
    print(f"[green]Built site → {out}[/green]")

if __name__ == "__main__":
    app()
