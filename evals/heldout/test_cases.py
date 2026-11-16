"""The held-out cases: definitions load, data is reproducible, planted answers
are real and each trap really catches a naive analysis

Generators are called directly, so no CSV is written to evals/data. To pick a
seed that passes a case's checks: PYTHONPATH=. python evals/heldout/test_cases.py h2
"""

import importlib.util
import sys
import warnings

import numpy as np
import pandas as pd
import pytest
import statsmodels.formula.api as smf
from scipy import stats

from evals import cases as cases_module
from evals.cases import all_cases, load_case
from evals.generators import GENERATORS as DEV_GENERATORS

warnings.filterwarnings("ignore", category=RuntimeWarning)

NAMES = ["h1", "h2", "h3", "h4"]


def _heldout_generators() -> dict:
    # Same directory the loader reads, so this checks what the harness will run
    path = cases_module.HELDOUT_DIR / "generators.py"
    spec = importlib.util.spec_from_file_location("heldout_generators", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GENERATORS


GENERATORS = _heldout_generators()


def data(name: str, seed: int | None = None) -> pd.DataFrame:
    case = load_case(name)
    return GENERATORS[case.data.generator](case.data.seed if seed is None else seed)


# ------------------------------------------------------------------ the cases


def check_h1(d):
    fit = smf.logit("repeat_visit ~ quarter + C(tier)", d).fit(disp=0)
    assert fit.params.quarter < 0 and fit.pvalues.quarter < 1e-4
    for tier, g in d.groupby("tier"):
        assert smf.logit("repeat_visit ~ quarter", g).fit(disp=0).params.quarter < 0, tier
    silver = d[d.tier == "silver"]
    assert silver[silver.quarter <= 2].repeat_visit.mean() > 0.45
    assert silver[silver.quarter >= 7].repeat_visit.mean() < 0.38
    rates = d.groupby("tier").repeat_visit.mean()
    assert rates.gold > rates.silver > rates.bronze
    # Trap: pooled over tiers, the trend runs the other way
    pooled = smf.logit("repeat_visit ~ quarter", d).fit(disp=0)
    assert pooled.params.quarter > 0 and pooled.pvalues.quarter < 1e-6


def check_h2(d):
    fit = smf.logit("renewed ~ discount_pct + support_tickets + np.log(seats)", d)
    fit = fit.fit(disp=0)
    assert fit.params.discount_pct < 0 and fit.pvalues.discount_pct < 1e-10
    assert fit.params.support_tickets > 0 and fit.pvalues.support_tickets < 1e-10
    assert fit.params["np.log(seats)"] > 0 and fit.pvalues["np.log(seats)"] < 1e-10
    # Stated as a finding, so it must hold at the seed
    for c in ["contract_months", "signup_month"]:
        assert stats.pointbiserialr(d.renewed, d[c]).pvalue > 0.2, c
    assert stats.chi2_contingency(pd.crosstab(d.region, d.renewed))[1] > 0.2
    # Trap: a magnitude ranking surfaces the right features, but carries no
    # sign, and the signs run against what the names suggest
    numeric = ["discount_pct", "seats", "support_tickets", "contract_months", "signup_month"]
    rho = {c: stats.spearmanr(d[c], d.renewed)[0] for c in numeric}
    top3 = sorted(numeric, key=lambda c: -abs(rho[c]))[:3]
    assert set(top3) == {"discount_pct", "seats", "support_tickets"}
    assert rho["discount_pct"] < 0 < rho["support_tickets"]


def check_h3(d):
    assert d.isna().sum().sum() == 0  # nothing a plain check calls missing
    zero = d.parcel_weight_kg == 0
    assert d.parcel_weight_kg[~zero].min() >= 0.2  # 0.0 sits apart from the rest
    gap = d.delivery_hours[zero].mean() - d.delivery_hours[~zero].mean()
    assert 25 < gap < 35
    assert stats.ttest_ind(d.delivery_hours[zero], d.delivery_hours[~zero]).pvalue < 1e-20
    fit = smf.ols("delivery_hours ~ parcel_weight_kg + distance_km", d[~zero]).fit()
    assert 1.2 < fit.params.parcel_weight_kg < 1.8 and fit.pvalues.parcel_weight_kg < 1e-20
    assert 0.04 < fit.params.distance_km < 0.06 and fit.pvalues.distance_km < 1e-20
    # Trap: with the zeros left in, weight looks like it speeds delivery up
    r, p = stats.pearsonr(d.parcel_weight_kg, d.delivery_hours)
    assert r < 0 and p < 0.01


def check_h4(d):
    got = d.extra_sessions == 1
    assert d.pre_score[got].max() <= d.pre_score[~got].min()
    gap = d.score_gain[got].mean() - d.score_gain[~got].mean()
    # Trap: the raw comparison credits the sessions with a large gain
    assert 5 < gap < 12
    assert stats.ttest_ind(d.score_gain[got], d.score_gain[~got]).pvalue < 1e-6
    r, p = stats.pearsonr(d.pre_score, d.score_gain)
    assert r < 0 and p < 1e-20
    fit = smf.ols("score_gain ~ pre_score + extra_sessions + attendance_pct", d).fit()
    assert fit.pvalues.extra_sessions > 0.05 and abs(fit.params.extra_sessions) < gap / 2
    assert fit.params.attendance_pct > 0 and fit.pvalues.attendance_pct < 1e-6


CHECKS = {"h1": check_h1, "h2": check_h2, "h3": check_h3, "h4": check_h4}


# ------------------------------------------------------------------ the tests


def test_held_out_cases_load():
    assert {c.name for c in all_cases("heldout")} == set(NAMES)
    for name in NAMES:
        assert load_case(name).name == name  # results name the case


def test_held_out_cases_stay_separate_from_the_dev_set():
    heldout = all_cases("heldout")
    assert not {c.name for c in heldout} & {c.name for c in all_cases()}
    assert not {c.data.generator for c in heldout} & set(DEV_GENERATORS)
    files = [c.file for c in heldout] + [c.file for c in all_cases()]
    assert len(set(files)) == len(files)


def test_file_names_dont_give_the_answer_away():
    for case in all_cases("heldout"):
        assert not set(case.name.split("_")) & set(case.file[:-4].split("_"))


@pytest.mark.parametrize("name", NAMES)
def test_generated_data_is_reproducible_and_sized_like_the_dev_cases(name):
    case = load_case(name)
    d = data(name)
    assert d.equals(data(name))
    assert case.target in d.columns
    assert 60 <= len(d) <= 2000 and 4 <= d.shape[1] <= 10
    assert 3 <= len(case.must_find) <= 5 and 1 <= len(case.must_not_claim) <= 2


@pytest.mark.parametrize(
    ("name", "fact", "compute"),
    [
        ("h1", "gold_share_q1", lambda d: (d[d.quarter == 1].tier == "gold").mean()),
        ("h1", "gold_share_q8", lambda d: (d[d.quarter == 8].tier == "gold").mean()),
        ("h2", "no_discount_renewal", lambda d: d[d.discount_pct == 0].renewed.mean()),
        ("h2", "top_discount_renewal", lambda d: d[d.discount_pct == 30].renewed.mean()),
        ("h3", "zero_weights", lambda d: (d.parcel_weight_kg == 0).sum()),
        ("h4", "extra_sessions_students", lambda d: d.extra_sessions.sum()),
    ],
)
def test_expected_facts_match_the_data(name, fact, compute):
    [expected] = [f for f in load_case(name).facts if f.name == fact]
    assert compute(data(name)) == pytest.approx(expected.value, rel=1e-5)


def test_every_fact_is_checked():
    checked = {
        (n, f) for n, f, _ in
        test_expected_facts_match_the_data.pytestmark[0].args[1]
    }
    assert {(n, f.name) for n in NAMES for f in load_case(n).facts} == checked


@pytest.mark.parametrize("name", NAMES)
def test_planted_answers_are_recoverable_and_the_trap_is_real(name):
    CHECKS[name](data(name))


if __name__ == "__main__":
    # First seed from 1 at which a case's checks pass; facts don't depend on it
    name = sys.argv[1]
    for seed in range(1, 1000):
        try:
            CHECKS[name](data(name, seed))
        except AssertionError:
            continue
        print(f"{name}: seed {seed} passes")
        break