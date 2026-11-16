"""The eval cases: definitions load, data is reproducible, planted answers are real

Each planted effect must be clearly recoverable with a plain test at the chosen
seed (and nothing found on pure_noise), or the case would grade the agent on
noise. Titanic's values come from the claim checks; the other downloaded cases
are checked here against their files (downloaded once, into evals/data).
"""

import hashlib
import io
import warnings
import zipfile

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
    if case.data.generator:
        return GENERATORS[case.data.generator](case.data.seed)
    return pd.read_csv(dataset(case))


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
        "penguins",
        "diabetes",
        "bike_sharing",
        "u_shape",
        "small_sample",
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
        ("u_shape", "outcome_rate", lambda d: d.outcome.mean()),
        ("small_sample", "mean_score", lambda d: d.score.mean()),
        ("penguins", "mean_mass", lambda d: d.body_mass_g.mean()),
        (
            "penguins",
            "gentoo_mass",
            lambda d: d[d.species == "Gentoo"].body_mass_g.mean(),
        ),
        (
            "penguins",
            "adelie_mass",
            lambda d: d[d.species == "Adelie"].body_mass_g.mean(),
        ),
        ("diabetes", "outcome_rate", lambda d: d.Outcome.mean()),
        ("diabetes", "insulin_zeros", lambda d: (d.Insulin == 0).sum()),
        ("diabetes", "skin_zeros", lambda d: (d.SkinThickness == 0).sum()),
        ("bike_sharing", "mean_cnt", lambda d: d.cnt.mean()),
        ("bike_sharing", "rentals_2011", lambda d: d[d.yr == 0].cnt.mean()),
        ("bike_sharing", "rentals_2012", lambda d: d[d.yr == 1].cnt.mean()),
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


def test_u_shape_is_missed_by_a_linear_test():
    d = data("u_shape")
    rates = d.groupby(pd.qcut(d.feat_a, 5), observed=True).outcome.mean().tolist()
    assert min(rates[0], rates[-1]) > 0.5 and rates[2] < 0.2
    assert stats.pointbiserialr(d.outcome, d.feat_a).pvalue > 0.5
    p = smf.logit("outcome ~ feat_a + I(feat_a**2) + feat_b + feat_c", d).fit(disp=0)
    assert p.pvalues["I(feat_a ** 2)"] < 1e-20 and p.pvalues.feat_b < 1e-6
    assert p.pvalues.feat_c > 0.2


def test_small_sample_has_one_effect_and_a_near_miss():
    d = data("small_sample")
    p = {c: stats.pearsonr(d[c], d.score).pvalue for c in d.columns if c != "score"}
    assert len(d) == 60 and p.pop("feat_1") < 0.01
    assert min(p.values()) > 0.05  # feat_3 at 0.063: close, not significant


def test_penguins_bill_depth_is_confounded_by_species():
    d = data("penguins").dropna(subset=["body_mass_g", "bill_depth_mm"])
    assert stats.pearsonr(d.bill_depth_mm, d.body_mass_g)[0] < -0.4
    for _, g in d.groupby("species"):
        assert stats.pearsonr(g.bill_depth_mm, g.body_mass_g)[0] > 0.5
    r = {c: d[c].corr(d.body_mass_g) for c in ["bill_length_mm", "flipper_length_mm"]}
    assert max(r, key=r.get) == "flipper_length_mm"
    mass = d.groupby("species").body_mass_g.mean()
    assert mass.idxmax() == "Gentoo" and mass.Gentoo - mass.drop("Gentoo").max() > 1000
    by_sex = d.groupby(["species", "sex"]).body_mass_g.mean().unstack()
    assert (by_sex.male > by_sex.female).all()


def test_diabetes_zeros_are_missing_values_that_hide_an_effect():
    d = data("diabetes")
    assert d.isna().sum().sum() == 0  # nothing a plain check calls missing
    zeros = (
        d[["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]] == 0
    ).sum()
    assert zeros.Insulin == 374 and zeros.SkinThickness == 227 and zeros.min() > 0
    r = {
        c: stats.pointbiserialr(d.Outcome, d[c])[0] for c in d.columns if c != "Outcome"
    }
    assert max(r, key=r.get) == "Glucose"
    assert r["BMI"] > 0.2 and r["Age"] > 0.2
    # With the zeros, blood pressure looks unrelated; without them, it isn't
    assert stats.pointbiserialr(d.Outcome, d.BloodPressure).pvalue > 0.05
    bp = d[d.BloodPressure > 0]
    assert (
        stats.ttest_ind(
            bp[bp.Outcome == 1].BloodPressure, bp[bp.Outcome == 0].BloodPressure
        ).pvalue
        < 1e-4
    )


def test_bike_sharing_leakage_and_effects():
    d = data("bike_sharing")
    assert (d.casual + d.registered == d.cnt).all()
    assert stats.pearsonr(d.temp, d.cnt)[0] > 0.5
    by_season = d.groupby("season").cnt.mean()
    assert by_season.idxmin() == 1 and set(d[d.season == 1].mnth) == {12, 1, 2, 3}
    by_weather = d.groupby("weathersit").cnt.mean()
    assert by_weather.is_monotonic_decreasing
    p = smf.ols("cnt ~ yr + temp + C(season) + C(weathersit)", d).fit().pvalues
    assert p.yr < 1e-50 and p.temp < 1e-10
    # Not an expected finding: the working-day difference is small
    assert (
        stats.ttest_ind(d[d.workingday == 1].cnt, d[d.workingday == 0].cnt).pvalue
        > 0.05
    )


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


def test_a_zip_download_is_checked_then_its_member_extracted(monkeypatch, tmp_path):
    csv = b"a,b\n1,2\n"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("Readme.txt", "r")
        z.writestr("day.csv", csv)
    content = buffer.getvalue()

    class Response:
        def __init__(self, body):
            self.content = body

    case = Case(
        name="dl",
        description="d",
        file="x.csv",
        target="b",
        data=Source(
            url="https://example.org/x.zip",
            sha256=hashlib.sha256(content).hexdigest(),
            member="day.csv",
        ),
        must_find=["x"],
    )
    monkeypatch.setattr(cases_module.httpx, "get", lambda *a, **k: Response(content))
    assert dataset(case, tmp_path).read_bytes() == csv


def test_a_case_needs_exactly_one_source():
    with pytest.raises(ValueError):
        Source(generator="pure_noise", seed=1, url="u", sha256="s")
    with pytest.raises(ValueError):
        Source()


@pytest.mark.parametrize(
    "suite, attribute", [("heldout", "HELDOUT_DIR"), ("heldout2", "HELDOUT2_DIR")]
)
def test_held_out_cases_load_from_their_own_directory(
    monkeypatch, tmp_path, suite, attribute
):
    (tmp_path / "cases").mkdir()
    (tmp_path / "generators.py").write_text(
        "import pandas as pd\n"
        "GENERATORS = {'hidden': lambda seed: pd.DataFrame({'y': [seed]})}\n"
    )
    (tmp_path / "cases" / "secret.yaml").write_text(
        "description: d\nfile: hidden.csv\ntarget: y\n"
        "data: {generator: hidden, seed: 3}\nmust_find: [x]\n"
    )
    monkeypatch.setattr(cases_module, attribute, tmp_path)
    assert [c.name for c in all_cases(suite)] == ["secret"]
    assert "secret" not in {c.name for c in all_cases()}
    case = load_case("secret")  # results name the case, so grading finds it
    assert pd.read_csv(dataset(case, tmp_path / "data")).y.tolist() == [3]
