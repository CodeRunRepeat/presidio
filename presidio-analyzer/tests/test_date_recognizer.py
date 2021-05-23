import pytest

from tests import assert_result_within_score_range
from presidio_analyzer.predefined_recognizers import DateRecognizer


@pytest.fixture(scope="module")
def recognizer():
    return DateRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["DATE_TIME"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions, expected_score_ranges",
    [
        # fmt: off
        # Date tests
        ("Today is 5-20-2021", 1, ((9, 18),), ((0.6, 0.81),),),
        ("Today is 5/20/2021", 1, ((9, 18),), ((0.6, 0.81),),),
        ("Today is 2021-05-21", 1, ((9, 19),), ((0.6, 0.81),),),
        ("Today is 21.5.2021", 1, ((9, 18),), ((0.6, 0.81),),),
        ("Today is 5-MAY-2021", 1, ((9, 19),), ((0.6, 0.81),),),
        # fmt: on
    ],
)
def test_when_all_dates_then_succeed(
    text,
    expected_len,
    expected_positions,
    expected_score_ranges,
    recognizer,
    entities,
    max_score,
):
    results = recognizer.analyze(text, entities)
    assert len(results) == expected_len
    for res, (st_pos, fn_pos), (st_score, fn_score) in zip(
        results, expected_positions, expected_score_ranges
    ):
        if fn_score == "max":
            fn_score = max_score
        assert_result_within_score_range(
            res, entities[0], st_pos, fn_pos, st_score, fn_score
        )
