from __future__ import annotations
from typing import List, Dict
import os
import html
from jinja2 import Environment, FileSystemLoader, select_autoescape  # Jinja2 env: https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.Environment
from .data import Product
from .config import AppCfg
from .model import generate_article_copy

def slugify(name: str) -> str:
    s = "".join(ch.lower() if ch.isalnum() else "-" for ch in name)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")

def build_site(cfg: AppCfg, products: List[Product], out_dir: str) -> None:
    env = Environment(
        loader=FileSystemLoader("referflow/templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    os.makedirs(out_dir, exist_ok=True)
    # Copy public assets
    src_css = "referflow/public/style.css"
    dst_css = os.path.join(out_dir, "style.css")
    with open(src_css, "rb") as r, open(dst_css, "wb") as w:
        w.write(r.read())

    # Render index
    index_tpl = env.get_template("index.html")
    index_html = index_tpl.render(
        cfg=cfg,
        products=[{"title": p.title, "slug": slugify(p.title), "price_eur": p.price_eur} for p in products],
    )
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Render articles
    art_tpl = env.get_template("article.html")
    for p in products:
        copy = generate_article_copy(cfg, p)
        html_out = art_tpl.render(cfg=cfg, p=p, copy=copy, slug=slugify(p.title))
        with open(os.path.join(out_dir, f"{slugify(p.title)}.html"), "w", encoding="utf-8") as f:
            f.write(html_out)
