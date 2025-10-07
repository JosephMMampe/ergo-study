from __future__ import annotations
import os
import shutil
from referflow.config import load_config
from referflow.data import load_products
from referflow.render import build_site

def test_build(tmp_path):
    out = tmp_path / "site"
    cfg = load_config("config.yaml")
    products = load_products("products.csv")
    build_site(cfg, products, str(out))
    assert (out / "index.html").exists()
    # Every product gets a page
    import glob
    pages = list(glob.glob(str(out / "*.html")))
    assert len(pages) >= 2
