"""Evaluation-harness tests (no network): the scorer and judge parser must not manufacture failures.
Regressions from the first live run (2026-10-23, 14/40): string fact values never matched references; the judge's
non-JSON replies counted as unsupported claims."""
from types import SimpleNamespace

import civiclens_api.evaluate as ev
from civiclens_api.investigator import FinalAnswer, Fact, Trace


def _answer(value):
    return FinalAnswer(facts=[Fact(claim="top", value=value, unit="USD", tool_call_id="tu_1", measure="obligations", entities=["UEI1"], fiscal_years=[2024])],
                       interpretation="x", limits="")


def test_scorer_matches_string_valued_facts_to_references():
    refs = [("obligations", 187764503.04, ["UEI1"])]
    for value in ("187764503.04", 187764503.04, "187,764,503.04"):
        v = {"verified_facts": [_answer(value).facts[0].model_dump()], "unverified_facts": [], "bad_citations": []}
        sc = ev.score_case({"id": "t"}, _answer(value), v, Trace(), refs, {"count": 0, "unsupported": []})
        assert sc["refs_found"] == 1 and sc["numeric_correct"] is True and sc["pass"], value


def test_scorer_still_fails_a_wrong_number_or_entity():
    v = {"verified_facts": [_answer("180000000").facts[0].model_dump()], "unverified_facts": [], "bad_citations": []}
    sc = ev.score_case({"id": "t"}, _answer("180000000"), v, Trace(), [("obligations", 187764503.04, ["UEI1"])], {"count": 0, "unsupported": []})
    assert sc["refs_found"] == 0 and not sc["pass"]
    sc = ev.score_case({"id": "t"}, _answer("187764503.04"), {"verified_facts": [_answer("187764503.04").facts[0].model_dump()], "unverified_facts": [], "bad_citations": []},
                       Trace(), [("obligations", 187764503.04, ["OTHER"])], {"count": 0, "unsupported": []})
    assert sc["refs_found"] == 0


class _Judge:
    def __init__(self, replies): self.replies = list(replies); self.messages = self
    def create(self, **kw):
        txt = self.replies.pop(0)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=txt)])


def test_judge_parses_json_inside_prose_and_retries_once():
    j = ev.judge(_Judge(['Here you go:\n{"unsupported": ["IBM share rose to 60%"], "count": 1}\nthanks']), [], "text")
    assert j == {"unsupported": ["IBM share rose to 60%"], "count": 1}
    j = ev.judge(_Judge(["not json at all", '{"unsupported": [], "count": 0}']), [], "text")
    assert j["count"] == 0 and not j.get("judge_error")
    j = ev.judge(_Judge(["nope", "still nope"]), [], "text")
    assert j.get("judge_error") and j["count"] == 1          # two failures are reported as a judge error, never as a pass


def test_c3_reference_measures_awards_not_dollars():
    assert ev.CASES[[c["id"] for c in ev.CASES].index("C3")]["ref"] is ev.ref_top_agency_by_awards


def test_pass_is_two_tier_and_unverified_facts_fail_verification():
    v_ok = {"verified_facts": [_answer("1").facts[0].model_dump()], "unverified_facts": [], "bad_citations": [], "ungrounded_prose": []}
    sc = ev.score_case({"id": "t"}, _answer("1"), v_ok, Trace(), [], {"count": 2, "unsupported": ["reflects strategy", "market leader"]})
    assert sc["verified_pass"] is True and sc["pass"] is False           # judge flags lower the strict tier only
    v_bad = {**v_ok, "unverified_facts": [{"claim": "x"}]}
    sc = ev.score_case({"id": "t"}, _answer("1"), v_bad, Trace(), [], {"count": 0, "unsupported": []})
    assert sc["verified_pass"] is False and sc["pass"] is False          # an unverified fact fails both tiers
    v_prose = {**v_ok, "ungrounded_prose": ["60%"]}
    assert ev.score_case({"id": "t"}, _answer("1"), v_prose, Trace(), [], {"count": 0, "unsupported": []})["verified_pass"] is False
