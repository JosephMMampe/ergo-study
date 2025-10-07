from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List
import pandas as pd  # pandas read_csv: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

@dataclass
class Product:
    title: str
    affiliate_url: str
    price_eur: float
    pros: str
    cons: str
    specs: str

def load_products(csv_path: str) -> List[Product]:
    df = pd.read_csv(csv_path)
    required = ["title","affiliate_url","price_eur","pros","cons","specs"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    out: List[Product] = []
    for _, row in df.iterrows():
        out.append(Product(
            title=str(row["title"]).strip(),
            affiliate_url=str(row["affiliate_url"]).strip(),
            price_eur=float(row["price_eur"]),
            pros=str(row["pros"]).strip(),
            cons=str(row["cons"]).strip(),
            specs=str(row["specs"]).strip(),
        ))
    if not out:
        raise ValueError("No products found in CSV.")
    return out
