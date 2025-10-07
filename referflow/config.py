from __future__ import annotations
from pydantic import BaseModel, Field

class ModelCfg(BaseModel):
    # Allow "model_name" without warning about protected namespace
    model_config = {"protected_namespaces": ()}
    provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 800

class ThemeCfg(BaseModel):
    brand_color: str = "#0f766e"
    accent_color: str = "#f59e0b"
    font_stack: str = "system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial"

class AppCfg(BaseModel):
    site_name: str
    site_tagline: str
    base_url: str
    dry_run: bool = True
    seed: int = 42
    model: ModelCfg = Field(default_factory=ModelCfg)
    theme: ThemeCfg = Field(default_factory=ThemeCfg)
    disclosure: str

def load_config(path: str) -> AppCfg:
    # PyYAML safe_load — docs: https://pyyaml.org/wiki/PyYAMLDocumentation
    import yaml  # provided by PyYAML (pip dist name: PyYAML)
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppCfg(**data)
