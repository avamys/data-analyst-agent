"""Eval cases: a dataset with known answers, defined in evals/cases/<name>.yaml

A case's data is generated from a seed (evals/generators.py) or downloaded and
checked against a SHA-256 checksum, and written to evals/data/<name>.csv.
"""

import hashlib
from pathlib import Path

import httpx
import yaml
from pydantic import BaseModel, model_validator

from evals.generators import GENERATORS

CASES_DIR = Path(__file__).parent / "cases"
DATA_DIR = Path(__file__).parent / "data"


class Source(BaseModel):
    """Where the data comes from: a generator and seed, or a URL and checksum"""

    generator: str | None = None
    seed: int | None = None
    url: str | None = None
    sha256: str | None = None

    @model_validator(mode="after")
    def _one_source(self):
        generated = self.generator in GENERATORS and self.seed is not None
        downloaded = bool(self.url and self.sha256)
        if generated == downloaded:
            raise ValueError(
                "Give either a known generator and a seed, or url and sha256"
            )
        return self


class Fact(BaseModel):
    """A value the report should state, on a line with one of its keywords"""

    name: str
    value: float
    near: list[str]


class Case(BaseModel):
    name: str
    description: str
    target: str
    data: Source
    facts: list[Fact] = []
    must_find: list[str]
    must_not_claim: list[str] = []
    # Caveat name -> keywords, any of which in the report counts as stating it
    caveats: dict[str, list[str]] = {}


def load_case(name: str) -> Case:
    spec = yaml.safe_load((CASES_DIR / f"{name}.yaml").read_text())
    return Case(name=name, **spec)


def all_cases() -> list[Case]:
    return [load_case(p.stem) for p in sorted(CASES_DIR.glob("*.yaml"))]


def dataset(case: Case, data_dir: Path = DATA_DIR) -> Path:
    """The case's CSV, generated or downloaded on first use"""
    path = data_dir / f"{case.name}.csv"
    if path.exists():
        return path
    data_dir.mkdir(parents=True, exist_ok=True)
    if case.data.generator:
        GENERATORS[case.data.generator](case.data.seed).to_csv(path, index=False)
        return path
    content = httpx.get(case.data.url, follow_redirects=True, timeout=60).content
    digest = hashlib.sha256(content).hexdigest()
    if digest != case.data.sha256:
        raise ValueError(
            f"{case.name}: download from {case.data.url} has sha256 {digest}"
        )
    path.write_bytes(content)
    return path
