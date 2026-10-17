import json, pathlib
import pytest
from rc_beam import calc, optimise

G = json.loads((pathlib.Path(__file__).parent / "golden_cases.json").read_text())
BASE = G["optimise"]["input"]


def test_factored_moment():
    assert calc(BASE)["Mu"] == pytest.approx(1.5 * (20 + 25 * .3 * .5) * 36 / 8)


def test_cantilever_moment():
    assert calc({**BASE, "type": "cant"})["Mu"] == pytest.approx(1.5 * (20 + 3.75) * 36 / 2)


@pytest.mark.parametrize("fy,coef", [(250, .148), (415, .138), (500, .133)])
def test_limiting_moment_coefficient(fy, coef):
    r = calc({**BASE, "fy": fy})
    assert r["Ml"] / (25 * 300 * r["d"] ** 2 / 1e6) == pytest.approx(coef, abs=.002)


def test_capacity_covers_demand():
    r = calc(BASE)
    assert r["pass"] and r["Mcap"] >= r["Mu"]


def test_doubly_reinforced_when_over_limit():
    r = calc({**BASE, "w": 60, "D": 400})
    assert r["dbl"] and r["Asc"] > 0


def test_t_beam_needs_no_more_steel_than_rectangle():
    t, rect = calc({**BASE, "sect": "T", "w": 35}), calc({**BASE, "w": 35})
    assert t["fl"] and t["Areq"] <= rect["Areq"] and t["Mcap"] >= t["Mu"]


def test_optimiser_sorted_and_passing():
    o = optimise(BASE)
    assert o and all(a["cost"] <= b["cost"] for a, b in zip(o, o[1:])) and all(r["pass"] for r in o)


@pytest.mark.parametrize("case", G["cases"], ids=lambda c: c["name"])
def test_golden(case):
    r, e = calc(case["input"]), case["expected"]
    if "fail" in e:
        assert r["fail"] == e["fail"]
        return
    for k, v in e.items():
        assert (r[k] == pytest.approx(v, rel=1e-9)) if isinstance(v, float) else (r[k] == v), k


from rc_beam import column

CB = G["columns"][0]["input"]


def test_column_axial_capacity_formula():
    r = column(CB)
    assert r["pass"] and r["Puz"] == pytest.approx((.45 * 25 * (300 * 450 - r["As"]) + .75 * 500 * r["As"]) / 1e3)


def test_minimum_eccentricity_governs_light_moments():
    r = column({**CB, "Mx": 0, "My": 0})
    assert r["Mxd"] == pytest.approx(r["Pu"] * max(3200 / 500 + 450 / 30, 20) / 1e3)


def test_slender_column_adds_moment():
    assert column({**CB, "Lx": 5.5})["Max"] > 0


def test_more_load_needs_no_less_steel():
    a, b = column(CB), column({**CB, "P": 1000})
    assert a["pass"] and b["pass"] and b["As"] >= a["As"] and a["ratio"] <= 1


@pytest.mark.parametrize("case", G["columns"], ids=lambda c: c["name"])
def test_column_golden(case):
    r, e = column(case["input"]), case["expected"]
    if "fail" in e:
        assert r["fail"] == e["fail"]
        return
    for k, v in e.items():
        assert (r[k] == pytest.approx(v, rel=1e-9)) if isinstance(v, float) else (r[k] == v), k


from rc_beam.core import tau_c


@pytest.mark.parametrize("pt,fck,table", [(.5, 25, .49), (1.0, 25, .64), (1.0, 20, .62), (.5, 20, .48)])
def test_shear_strength_matches_table_19(pt, fck, table):
    assert tau_c(pt, fck) == pytest.approx(table, abs=.02)


def test_stirrup_zones_group_into_at_most_three_and_widen_to_midspan():
    z = calc({**BASE, "w": 120, "L": 3.5, "b": 350})["zones"]
    assert 1 < len(z) <= 3 and [a[2] for a in z] == sorted(a[2] for a in z)


def test_curtailment_keeps_at_least_half_the_bars():
    r = calc(BASE)
    assert r["ca"] and r["ca"][0] >= 2 and 0 <= r["ca"][2] < r["ca"][1]


def test_seismic_option_adds_member_checks():
    assert len(calc({**BASE, "eq": 1})["checks"]) == len(calc(BASE)["checks"]) + 4
