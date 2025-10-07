from __future__ import annotations
import importlib
import hashlib
import random
from importlib import metadata
from typing import Dict, Tuple

# pip package name -> (import module name)
PKG_IMPORTS: Dict[str, str] = {
    "openai": "openai",
    "pandas": "pandas",
    "Jinja2": "jinja2",   # pip name is Jinja2, module is jinja2
    "PyYAML": "yaml",     # pip name is PyYAML, module is yaml
    "markdown": "markdown",
    "typer": "typer",
    "rich": "rich",
    "pydantic": "pydantic",
}

# Expected pinned versions (must match requirements.txt exactly)
PINNED: Dict[str, str] = {
    "openai": "1.51.2",
    "pandas": "2.2.2",
    "Jinja2": "3.1.4",
    "PyYAML": "6.0.2",
    "markdown": "3.6",
    "typer": "0.12.4",
    "rich": "13.7.1",
    "pydantic": "2.9.2",
}

def assert_versions() -> None:
    """
    Fail fast with human-readable errors if installed dists differ from pins.
    Uses importlib.metadata (robust) instead of module.__version__.
    Also verifies the import module actually imports.
    """
    errors = []
    for dist_name, expected in PINNED.items():
        # Check distribution version via importlib.metadata
        try:
            installed = metadata.version(dist_name)
        except metadata.PackageNotFoundError:
            errors.append(f"- Missing package: {dist_name} (expected {expected}). Install with `pip install -r requirements.txt`.")
            continue
        if installed != expected:
            errors.append(f"- Version mismatch for {dist_name}: expected {expected}, got {installed}. Recreate venv and `pip install -r requirements.txt`.")
        # Check import module loads
        mod_name = PKG_IMPORTS[dist_name]
        try:
            importlib.import_module(mod_name)
        except Exception as e:
            errors.append(f"- Installed but failed to import `{mod_name}` for {dist_name}: {e!r}")
    if errors:
        raise RuntimeError("Environment version check failed:\n" + "\n".join(errors))

def seeded_text(seed: int, title: str, n_sentences: int = 6) -> str:
    """Deterministic pseudo-content for DRY_RUN builds."""
    rnd = random.Random(int(hashlib.sha256(f"{seed}:{title}".encode()).hexdigest(), 16))
    phrases = [
        "Setup takes under five minutes",
        "Build quality is acceptable at this price",
        "The ergonomics improve neck comfort",
        "Cable management is straightforward",
        "Stability is fine for typical usage",
        "Consider pairing with a keyboard tray",
        "Measurements match the listing",
        "Value is the main selling point",
    ]
    return ". ".join(rnd.sample(phrases, k=min(n_sentences, len(phrases)))) + "."
