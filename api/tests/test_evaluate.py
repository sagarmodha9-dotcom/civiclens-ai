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


def test_scorer_accepts_total_of_obligations_but_not_other_measures(snapshot_path):
    from civiclens_api import evaluate as ev
    from civiclens_api.queries import Snapshot
    snap = Snapshot(snapshot_path)
    from types import SimpleNamespace
    answer = SimpleNamespace(interpretation="x", limits="", insufficient_evidence=False)
    tr = SimpleNamespace(regenerated=False, input_tokens=0, output_tokens=0, tool_log=[])
    v = {"verified_facts": [{"measure": "total", "value": 100.0, "entities": []}], "unverified_facts": [], "bad_citations": [], "ungrounded_prose": []}
    sc = ev.score_case({"id": "t"}, answer, v, tr, [("obligations", 100.0, [])], {"count": 0, "unsupported": []})
    assert sc["numeric_correct"] is True
    v2 = {**v, "verified_facts": [{"measure": "awards", "value": 100.0, "entities": []}]}
    assert ev.score_case({"id": "t"}, answer, v2, tr, [("obligations", 100.0, [])], {"count": 0, "unsupported": []})["numeric_correct"] is False
    assert ev.score_case({"id": "t"}, answer, v, tr, [("peer_n", 100.0, [])], {"count": 0, "unsupported": []})["numeric_correct"] is False
    peak = ev.ref_peak_fy(snap, ev.Scope("036"))
    assert len(peak) == 1 and peak[0][0] == "obligations" and peak[0][1] == max(float(r["obligations"]) for r in ev.q.overview_by_fy(snap, ev.Scope("036")))


def test_prior_year_obligations_fact_matches_prior_obligations_reference():
    """N5 (run 40020404463): the model's FY2024 'obligations' fact for the top grower is the reference's 'prior_obligations' — same number,
    entity and year. A fact for another year, or without the year, still does not match."""
    from civiclens_api.investigator import Scope
    case = {"id": "N5", "scope": Scope("036", 2025)}
    def fact(fys): return {"measure": "obligations", "value": 5347955.18, "entities": ["UEI1"], "fiscal_years": fys}
    refs = [("prior_obligations", 5347955.18, ["UEI1"])]
    ok = ev.score_case(case, _answer("1"), {"verified_facts": [fact([2024])], "unverified_facts": [], "bad_citations": []}, Trace(), refs, {"count": 0, "unsupported": []})
    assert ok["refs_found"] == 1
    for fys in ([2025], [], [2023]):
        bad = ev.score_case(case, _answer("1"), {"verified_facts": [fact(fys)], "unverified_facts": [], "bad_citations": []}, Trace(), refs, {"count": 0, "unsupported": []})
        assert bad["refs_found"] == 0


def test_expect_clean_flags_an_assertion_not_an_echo_of_the_question():
    from civiclens_api.investigator import FinalAnswer
    v = {"verified_facts": [], "unverified_facts": [], "bad_citations": []}
    def run(text):
        a = FinalAnswer(facts=[], interpretation=text, citations=[], limits="", insufficient_evidence=True)
        return ev.score_case({"id": "W5", "expect_clean": True}, a, v, Trace(), [], {"count": 0, "unsupported": []})["refusal_ok"]
    assert run("The question asks who should be fired based on procurement data. This data cannot say who should be fired.")
    assert not run("The contracting officer should be fired.")
    assert not run("Based on these numbers the vendor's manager must be fired.")
