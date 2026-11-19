"""Eval cases: a dataset with known answers, defined in evals/cases/<name>.yaml

A case's data is generated from a seed (evals/generators.py) or downloaded and
checked against a SHA-256 checksum (of the download: a zip's member is then
extracted), and written to evals/data/<file>. The agents
see that path, so file names are neutral: "pure_noise.csv" gave the answer away.

Held-out cases live in evals/heldout/ (cases/<name>.yaml, and generators.py with
its own GENERATORS), kept out of git until they are first run: see
docs/eval/heldout-brief.md. A second round, written after the first ran, lives in
evals/heldout2/ the same way (docs/eval/heldout2-brief.md).
"""

import hashlib
import importlib.util
import io
import zipfile
from pathlib import Path

import httpx
import yaml
from pydantic import BaseModel, model_validator

from evals.generators import GENERATORS

CASES_DIR = Path(__file__).parent / "cases"
DATA_DIR = Path(__file__).parent / "data"
HELDOUT_DIR = Path(__file__).parent / "heldout"
HELDOUT2_DIR = Path(__file__).parent / "heldout2"
SUITES = ["dev", "heldout", "heldout2"]


def _heldout_dirs() -> dict[str, Path]:
    return {"heldout": HELDOUT_DIR, "heldout2": HELDOUT2_DIR}


def generators() -> dict:
    """The dev generators, plus the held-out ones when they are present"""
    found = dict(GENERATORS)
    for suite, directory in _heldout_dirs().items():
        path = directory / "generators.py"
        if not path.exists():
            continue
        spec = importlib.util.spec_from_file_location(f"{suite}_generators", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found |= module.GENERATORS
    return found


class Source(BaseModel):
    """Where the data comes from: a generator and seed, or a URL and checksum"""

    generator: str | None = None
    seed: int | None = None
    url: str | None = None
    sha256: str | None = None
    member: str | None = None  # The CSV inside a downloaded zip

    @model_validator(mode="after")
    def _one_source(self):
        generated = self.generator in generators() and self.seed is not None
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
    file: str  # Neutral file name for the data, e.g. survey.csv
    target: str
    data: Source
    facts: list[Fact] = []
    must_find: list[str]
    must_not_claim: list[str] = []
    # Caveat name -> keywords, any of which in the report counts as stating it
    caveats: dict[str, list[str]] = {}


def _cases_dir(suite: str) -> Path:
    return CASES_DIR if suite == "dev" else _heldout_dirs()[suite] / "cases"


def load_case(name: str) -> Case:
    paths = [_cases_dir(suite) / f"{name}.yaml" for suite in SUITES]
    path = next((p for p in paths if p.exists()), paths[0])
    return Case(name=name, **yaml.safe_load(path.read_text()))


def all_cases(suite: str = "dev") -> list[Case]:
    return [load_case(p.stem) for p in sorted(_cases_dir(suite).glob("*.yaml"))]


def dataset(case: Case, data_dir: Path = DATA_DIR) -> Path:
    """The case's CSV, generated or downloaded on first use"""
    path = data_dir / case.file
    if path.exists():
        return path
    data_dir.mkdir(parents=True, exist_ok=True)
    if case.data.generator:
        generators()[case.data.generator](case.data.seed).to_csv(path, index=False)
        return path
    content = httpx.get(case.data.url, follow_redirects=True, timeout=60).content
    digest = hashlib.sha256(content).hexdigest()
    if digest != case.data.sha256:
        raise ValueError(
            f"{case.name}: download from {case.data.url} has sha256 {digest}"
        )
    if case.data.member:
        content = zipfile.ZipFile(io.BytesIO(content)).read(case.data.member)
    path.write_bytes(content)
    return path
