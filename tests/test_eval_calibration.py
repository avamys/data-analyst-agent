import json

import pytest
import yaml

from evals import calibration
from evals.calibration import agreement, calibrate, compare, load
from evals.cases import load_case
from evals.judge import PROMPT_VERSION

CASE = load_case("leakage")  # 5 findings, 2 forbidden claims, 1 caveat


def labels(find=("yes",) * 5, claims=(False, False), caveats=(True,)):
    """labels.yaml content as written by hand: unquoted yes / no included"""
    return {
        "case": "leakage",
        "source": "evals/runs/x/report.md",
        "must_find": [
            {"item": i, "label": x} for i, x in zip(CASE.must_find, find, strict=True)
        ],
        "must_not_claim": [
            {"item": i, "label": x}
            for i, x in zip(CASE.must_not_claim, claims, strict=True)
        ],
        "caveats": [
            {"item": i, "label": x} for i, x in zip(CASE.caveats, caveats, strict=True)
        ],
    }


def judged(find=("yes",) * 5, claims=("no", "no"), caveats=("yes",)):
    def v(x):
        return {"verdict": x, "quote": "q", "reason": "r"}

    return {
        "prompt": PROMPT_VERSION,
        "must_find": [v(x) for x in find],
        "must_not_claim": [v(x) for x in claims],
        "caveats": [v(x) for x in caveats],
    }


def write(path, content):
    path.mkdir(parents=True, exist_ok=True)
    (path / "labels.yaml").write_text(yaml.safe_dump(content))
    (path / "report.md").write_text("# Report\n")


def test_labels_load_and_yaml_booleans_become_verdicts(tmp_path):
    write(tmp_path / "r", labels())
    loaded, case = load(tmp_path / "r")
    assert case.name == "leakage"
    assert [x.label for x in loaded.must_not_claim] == ["no", "no"]
    assert loaded.caveats[0].label == "yes"


def test_labels_must_match_the_cases_items(tmp_path):
    content = labels()
    content["must_find"][2]["item"] = "An edited finding"
    write(tmp_path / "r", content)
    with pytest.raises(ValueError, match="must_find labels don't match"):
        load(tmp_path / "r")
    content = labels()
    content["must_find"].pop()
    write(tmp_path / "r", content)
    with pytest.raises(ValueError, match="must_find"):
        load(tmp_path / "r")


def test_agreement_is_exact_and_within_half(tmp_path):
    write(tmp_path / "r", labels(find=("yes", "partly", "no", "yes", "yes")))
    loaded, _ = load(tmp_path / "r")
    rows = compare(loaded, judged(find=("yes", "yes", "yes", "yes", "partly")))
    a = agreement(rows)
    assert a["must_find"] == {"items": 5, "exact": 2 / 5, "within_half": 4 / 5}
    assert a["must_not_claim"]["exact"] == 1.0
    assert a["all"] == {"items": 8, "exact": 5 / 8, "within_half": 7 / 8}
    [no_vs_yes] = [r for r in rows if not r["within_half"]]
    assert (no_vs_yes["label"], no_vs_yes["verdict"]) == ("no", "yes")


def test_stored_verdicts_are_reused_until_the_rubric_changes(monkeypatch, tmp_path):
    write(tmp_path / "a", labels())
    write(tmp_path / "b", labels())
    (tmp_path / "a" / "judge.json").write_text(json.dumps(judged()))
    (tmp_path / "b" / "judge.json").write_text(
        json.dumps({**judged(), "prompt": "older"})
    )
    calls = []

    def fake_judge(case, report, **trace):
        calls.append(trace["metadata"]["calibration"])
        return judged(find=("no",) * 5)

    monkeypatch.setattr(calibration, "judge", fake_judge)
    rows = calibrate(tmp_path, jobs=2)
    assert calls == ["b"]
    assert len(rows) == 16 and {r["report"] for r in rows} == {"a", "b"}
    stored = json.loads((tmp_path / "b" / "judge.json").read_text())
    assert stored["must_find"][0]["verdict"] == "no"
    calibrate(tmp_path, force=True)
    assert sorted(calls) == ["a", "b", "b"]


def test_invalid_labels_stop_before_any_judge_call(monkeypatch, tmp_path):
    write(tmp_path / "a", labels())
    content = labels()
    content["case"] = "titanic"
    write(tmp_path / "b", content)
    monkeypatch.setattr(calibration, "judge", lambda *a, **k: pytest.fail("judged"))
    with pytest.raises(ValueError, match="b: must_find"):
        calibrate(tmp_path)
