from __future__ import annotations
import os
from typing import Dict
from .utils import seeded_text

def generate_copy_openai(model_name: str, temperature: float, max_tokens: int, prompt: str) -> str:
    """
    OpenAI Python SDK v1 pattern:
    - Instantiate client: `from openai import OpenAI; client = OpenAI()`
    - Chat completion: `client.chat.completions.create(model=..., messages=[...])`
      Docs: https://platform.openai.com/docs/api-reference/chat/create
    """
    from openai import OpenAI  # openai==1.51.2
    client = OpenAI()  # Uses OPENAI_API_KEY env; docs: https://platform.openai.com/docs/quickstart?context=python
    resp = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": "You are a concise product reviewer. Write in clear, neutral, useful language with skimmable structure."},
            {"role": "user", "content": prompt},
        ],
    )
    # API shape: `resp.choices[0].message.content` (see doc above)
    return resp.choices[0].message.content or ""

def generate_article_copy(cfg, product) -> Dict[str, str]:
    base_prompt = (
        f"Product: {product.title}\n"
        f"Price (EUR): {product.price_eur}\n"
        f"Pros: {product.pros}\n"
        f"Cons: {product.cons}\n"
        f"Specs: {product.specs}\n\n"
        "Write: (1) a 150-200 word overview, (2) bullet pros/cons, "
        "(3) a short 'Who should buy this' paragraph, (4) a one-sentence verdict. "
        "Avoid hype; be actionable. EU market."
    )
    if cfg.dry_run or not os.getenv("OPENAI_API_KEY"):
        body = seeded_text(cfg.seed, product.title, n_sentences=6)
        overview = body
        who = "Best for students in small rooms seeking a simple, cheap ergonomic upgrade."
        verdict = "Good value if you accept limits."
    else:
        text = generate_copy_openai(
            cfg.model.model_name, cfg.model.temperature, cfg.model.max_tokens, base_prompt
        )
        # naive splits are fine; structure in template handles formatting
        overview = text
        who = "Who should buy: see summary."
        verdict = "Verdict: see summary."
    return {
        "overview": overview,
        "who": who,
        "verdict": verdict,
    }
