"""h5: the definition loads, data is reproducible, planted answers are real and
the trap really catches a naive analysis

Generators are called directly, so no CSV is written to evals/data. To pick a
seed that passes the checks: PYTHONPATH=. python evals/heldout2/test_h5.py
"""

import importlib.util
import warnings
from pathlib import Path

import pandas as pd
import pytest
import statsmodels.formula.api as smf
from scipy import stats

from evals import cases as cases_module
from evals.cases import all_cases, load_case
from evals.generators import GENERATORS as DEV_GENERATORS

warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = Path(__file__).resolve().parent
PLACEHOLDER = 99
FORMULA = "stay_rating ~ agency + website + superior + suite + nights + guests + lead_time_days"


def _generators(path: Path, module_name: str) -> dict:
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GENERATORS


GENERATORS = _generators(HERE / "generators.py", "heldout2_generators")
HELDOUT_GENERATORS = _generators(
    cases_module.HELDOUT_DIR / "generators.py", "heldout_generators_for_h5"
)


def data(seed: int | None = None) -> pd.DataFrame:
    case = load_case("h5")
    return GENERATORS[case.data.generator](case.data.seed if seed is None else seed)


def _dummies(d: pd.DataFrame) -> pd.DataFrame:
    return d.assign(
        agency=(d.booking_channel == "agency").astype(int),
        website=(d.booking_channel == "website").astype(int),
        superior=(d.room_type == "superior").astype(int),
        suite=(d.room_type == "suite").astype(int),
    )


# ------------------------------------------------------------------ the case


def check_h5(d):
    assert d.isna().sum().sum() == 0  # nothing a plain check calls missing
    unrated = d.stay_rating == PLACEHOLDER
    rated = d[~unrated]
    assert rated.stay_rating.between(1, 10).all()  # 99 sits apart from the rest
    # The profile shows 99 as the max, not as the most common value
    assert d.stay_rating.max() == PLACEHOLDER and d.stay_rating.median() <= 10
    assert d.stay_rating.mode()[0] != PLACEHOLDER
    # Missing ratings are concentrated in agency bookings
    share = unrated.groupby(d.booking_channel).mean()
    assert share.agency > 0.3 and share.direct < 0.1 and share.website < 0.1
    assert stats.chi2_contingency(pd.crosstab(d.booking_channel, unrated))[1] < 1e-10
    # Among rated stays: agency ~1 point below direct, suites ~1 point above standard
    fit = smf.ols(FORMULA, _dummies(rated)).fit()
    assert -1.6 < fit.params.agency < -0.6 and fit.pvalues.agency < 1e-8
    assert 0.6 < fit.params.suite < 1.6 and fit.pvalues.suite < 1e-6
    # Trap: with the 99s left in, agency guests look far happier
    agency = d.stay_rating[d.booking_channel == "agency"]
    direct = d.stay_rating[d.booking_channel == "direct"]
    assert agency.mean() > direct.mean() + 10
    assert stats.ttest_ind(agency, direct, equal_var=False).pvalue < 1e-8
    naive = smf.ols(FORMULA, _dummies(d)).fit()
    assert naive.params.agency > 5 and naive.pvalues.agency < 1e-8


FACTS = {"unrated_stays": lambda d: (d.stay_rating == PLACEHOLDER).sum()}


# ------------------------------------------------------------------ the tests


def test_case_loads():
    assert {c.name for c in all_cases("heldout2")} == {"h5"}
    assert load_case("h5").name == "h5"


def test_case_stays_separate_from_the_other_cases():
    case = load_case("h5")
    others = [*all_cases(), *all_cases("heldout")]
    assert case.name not in {c.name for c in others}
    assert case.file not in {c.file for c in others}  # the harness would reuse that CSV
    assert case.data.generator not in set(DEV_GENERATORS) | set(HELDOUT_GENERATORS)


def test_names_dont_give_the_answer_away():
    case = load_case("h5")
    for name in [case.file, *data().columns]:
        assert not any(w in name.lower() for w in ("missing", "unknown", "code", "flag")), name
    assert not set(case.name.split("_")) & set(case.file[:-4].split("_"))


def test_generated_data_is_reproducible_and_sized_like_the_dev_cases():
    case = load_case("h5")
    d = data()
    assert d.equals(data())
    assert not d.equals(data(case.data.seed + 1))
    assert case.target in d.columns
    assert 60 <= len(d) <= 2000 and 4 <= d.shape[1] <= 10
    assert 3 <= len(case.must_find) <= 5 and 1 <= len(case.must_not_claim) <= 2


def test_expected_facts_match_the_data():
    facts = load_case("h5").facts
    assert {f.name for f in facts} == set(FACTS)  # every fact is checked
    d = data()
    for f in facts:
        assert FACTS[f.name](d) == pytest.approx(f.value, rel=1e-5), f.name


def test_planted_answers_are_recoverable_and_the_trap_is_real():
    check_h5(data())


if __name__ == "__main__":
    # First seed from 1 at which the checks pass; facts don't depend on it
    for seed in range(1, 1000):
        try:
            check_h5(data(seed))
        except AssertionError:
            continue
        print(f"h5: seed {seed} passes")
        break