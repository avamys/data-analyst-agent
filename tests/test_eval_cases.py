"""The eval cases: definitions load, data is reproducible, planted answers are real

Each planted effect must be clearly recoverable with a plain test at the chosen
seed (and nothing found on pure_noise), or the case would grade the agent on
noise. Titanic's data is downloaded, so its values come from the claim checks.
"""

import hashlib
import warnings

import numpy as np
import pandas as pd
import pytest
import statsmodels.formula.api as smf
from scipy import stats

from agent.profiling import auto_profile_dataset
from evals import cases as cases_module
from evals.cases import Case, Source, all_cases, dataset, load_case
from evals.generators import GENERATORS

warnings.filterwarnings("ignore", category=RuntimeWarning)


def data(name: str) -> pd.DataFrame:
    case = load_case(name)
    return GENERATORS[case.data.generator](case.data.seed)


def test_all_cases_load():
    names = {c.name for c in all_cases()}
    assert names == {
        "titanic",
        "planted_effects",
        "pure_noise",
        "leakage",
        "regression_outliers",
        "string_target",
        "datetime_trend",
    }


def test_file_names_dont_give_the_answer_away():
    # The agents see the path: a report cited "the file name, pure_noise"
    for case in all_cases():
        if case.name != "titanic":  # a real dataset under its own name
            assert not set(case.name.split("_")) & set(case.file[:-4].split("_"))
    assert len({c.file for c in all_cases()}) == len(all_cases())


@pytest.mark.parametrize("name", list(GENERATORS))
def test_generated_data_is_reproducible_and_has_the_target(name):
    case = load_case(name)
    assert data(name).equals(data(name))
    assert case.target in data(name).columns


@pytest.mark.parametrize(
    ("name", "fact", "compute"),
    [
        ("planted_effects", "outcome_rate", lambda d: d.outcome.mean()),
        ("planted_effects", "feat_d_missing", lambda d: d.feat_d.isna().mean()),
        ("pure_noise", "outcome_rate", lambda d: d.outcome.mean()),
        ("leakage", "churn_rate", lambda d: d.churned.mean()),
        (
            "leakage",
            "refund_agreement",
            lambda d: (d.refund_issued == d.churned).mean(),
        ),
        ("leakage", "basic_plan_churn", lambda d: d[d.plan == "basic"].churned.mean()),
        ("regression_outliers", "median_price", lambda d: d.price.median()),
        ("regression_outliers", "mean_price", lambda d: d.price.mean()),
        ("string_target", "churn_rate", lambda d: (d.churned_flag == "yes").mean()),
        (
            "string_target",
            "monthly_churn",
            lambda d: (d[d.contract == "monthly"].churned_flag == "yes").mean(),
        ),
        (
            "string_target",
            "annual_churn",
            lambda d: (d[d.contract == "annual"].churned_flag == "yes").mean(),
        ),
        ("datetime_trend", "mean_sales", lambda d: d.sales.mean()),
        (
            "datetime_trend",
            "weekend_sales",
            lambda d: d[pd.to_datetime(d.date).dt.dayofweek >= 5].sales.mean(),
        ),
        (
            "datetime_trend",
            "weekday_sales",
            lambda d: d[pd.to_datetime(d.date).dt.dayofweek < 5].sales.mean(),
        ),
    ],
)
def test_expected_facts_match_the_data(name, fact, compute):
    # Stored precisely: a report's value passes if the true value rounds to it
    [expected] = [f for f in load_case(name).facts if f.name == fact]
    assert compute(data(name)) == pytest.approx(expected.value, rel=1e-5)


def test_planted_effects_are_recoverable():
    d = data("planted_effects").dropna()
    p = smf.logit("outcome ~ feat_a + feat_b + feat_c + feat_d", d).fit(disp=0).pvalues
    assert p.feat_a < 1e-10 and p.feat_d < 1e-6 and p.feat_b < 0.01
    assert p.feat_c > 0.2
    # feat_b also shows up in a plain two-group comparison
    assert (
        stats.ttest_ind(d[d.outcome == 1].feat_b, d[d.outcome == 0].feat_b).pvalue
        < 0.01
    )


def test_pure_noise_has_nothing_to_find():
    d = data("pure_noise")
    features = [f"feat_{i}" for i in range(1, 6)]
    p = [
        stats.ttest_ind(d[d.outcome == 1][c], d[d.outcome == 0][c]).pvalue
        for c in features
    ]
    p.append(stats.chi2_contingency(pd.crosstab(d.group, d.outcome))[1])
    assert min(p) > 0.2


def test_leakage_is_flagged_by_the_profile_and_real_effects_exist():
    d = data("leakage")
    assert (
        "refund_issued" in auto_profile_dataset(d, "x.csv", "churned").leakage_suspects
    )
    p = (
        smf.logit("churned ~ usage_hours + tenure_months + C(plan)", d)
        .fit(disp=0)
        .pvalues
    )
    assert p.usage_hours < 1e-6 and p.tenure_months < 1e-4
    assert p.filter(like="plan").min() < 1e-3


def test_regression_effects_and_skew():
    d = data("regression_outliers")
    p = smf.ols("np.log(price) ~ size_sqm + age_years + rating", d).fit().pvalues
    assert p.size_sqm < 1e-20 and p.age_years < 1e-4 and p.rating > 0.2
    assert stats.skew(d.price) > 2


def test_string_target_effects_and_binary_detection():
    d = data("string_target")
    assert auto_profile_dataset(d, "x.csv", "churned_flag").target_type == "binary"
    d = d.assign(y=(d.churned_flag == "yes").astype(int))
    p = smf.logit("y ~ monthly_fee + support_calls + C(contract) + C(region)", d)
    p = p.fit(disp=0).pvalues
    assert p.monthly_fee < 1e-3 and p.support_calls < 1e-6
    assert p.filter(like="contract").min() < 1e-6
    assert stats.chi2_contingency(pd.crosstab(d.region, d.y))[1] > 0.2


def test_datetime_trend_effects():
    d = data("datetime_trend")
    d = d.assign(t=np.arange(len(d)), weekend=pd.to_datetime(d.date).dt.dayofweek >= 5)
    p = smf.ols("sales ~ t + weekend + promo + temperature", d).fit().pvalues
    assert p.t < 1e-20 and p["weekend[T.True]"] < 1e-20 and p.promo < 1e-10
    assert p.temperature > 0.2
    assert stats.pearsonr(d.temperature, d.sales).pvalue > 0.2


def test_generated_dataset_is_written_once(tmp_path):
    path = dataset(load_case("pure_noise"), tmp_path)
    assert pd.read_csv(path).equals(data("pure_noise"))


def test_downloads_are_checked_against_their_checksum(monkeypatch, tmp_path):
    content = b"a,b\n1,2\n"

    class Response:
        def __init__(self, body):
            self.content = body

    case = Case(
        name="dl",
        description="d",
        file="x.csv",
        target="b",
        data=Source(
            url="https://example.org/x.csv", sha256=hashlib.sha256(content).hexdigest()
        ),
        must_find=["x"],
    )
    monkeypatch.setattr(cases_module.httpx, "get", lambda *a, **k: Response(content))
    assert dataset(case, tmp_path).read_bytes() == content

    monkeypatch.setattr(cases_module.httpx, "get", lambda *a, **k: Response(b"other"))
    with pytest.raises(ValueError, match="sha256"):
        dataset(case.model_copy(update={"file": "y.csv"}), tmp_path)


def test_a_case_needs_exactly_one_source():
    with pytest.raises(ValueError):
        Source(generator="pure_noise", seed=1, url="u", sha256="s")
    with pytest.raises(ValueError):
        Source()
