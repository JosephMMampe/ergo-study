from __future__ import annotations
from referflow.render import slugify

def test_slugify_basic():
    assert slugify("Hello World!") == "hello-world"

def test_slugify_collapse():
    assert slugify("A  B   C") == "a-b-c"
