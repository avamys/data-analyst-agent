import pytest

from agent.number_check import (
    code_literals,
    numbers_in,
    recorded_values,
    unmatched_numbers,
)


def written(text):
    return [n for n, _, _, _ in numbers_in(text)]


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("survival is 74.2% here", 0.742038),  # a share written as a percentage
        ("missing 19.9%", 19.87),  # a percentage recorded as one
        ("891 passengers", 891),
        ("1,234 rows", 1234),
        ("V = 0.543", 0.5431),
        ("mean difference −2.28 years", -2.2822),  # sign is not compared
        ("p = 2.6e-58", 2.64e-58),
        ("p = 1.2 × 10⁻⁵⁸", 1.2e-58),
        ("a gap of 46.8 points", 0.46797),
        ("median 26", 26.28),  # rounded to the precision shown
    ],
)
def test_numbers_that_round_from_a_value_pass(text, value):
    assert unmatched_numbers(text, [value]) == []


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("survival is 74.3%", 0.742038),
        ("V = 0.55", 0.543),
        ("p = 3.7e-58", 3.7e-59),  # off by an order of magnitude
        ("891 passengers", 890),
    ],
)
def test_numbers_that_no_value_rounds_to_are_reported(text, value):
    [(number, line)] = unmatched_numbers(text, [value])
    assert number in text and line == text


def test_structural_numbers_are_not_checked():
    text = (
        "1. Class 3 has df = 2 in `eda_1.rate_3` (see eda_1, stat_2)\n"
        "p < 0.001 and 95% CI at alpha 0.05\n"
        "![chart](tasks/eda_1/charts/rate_by_class_2024.png)"
    )
    assert written(text) == []


def test_ranges_are_checked_number_by_number():
    assert written("OR 1.81 (1.16 to 2.83), IQR 19–36") == [
        "1.81",
        "1.16",
        "2.83",
        "19",
        "36",
    ]


def test_values_are_collected_from_nested_facts():
    fact = {"acc": 0.81, "top": {"Sex": -2.5}, "ns": [12, "0.3", "x"], "ok": True}
    assert sorted(recorded_values(fact)) == [0.3, 0.81, 2.5, 12.0]


def test_numbers_inside_strings_and_keys_count():
    # Grouped results: interval labels as values or keys; ids don't count
    fact = {"edges": ["(7.91, 14.454]"], "(14.454, 31.0]": 0.45, "age_0_16": 0.58}
    assert sorted(recorded_values(fact)) == [0.45, 0.58, 7.91, 14.454, 14.454, 31.0]


def test_code_literals_count_as_recorded():
    code = "train_test_split(X, y, test_size=0.25, random_state=42)\nx1 = 1e-3"
    assert unmatched_numbers("25% test, seed 42", code_literals(code)) == []
