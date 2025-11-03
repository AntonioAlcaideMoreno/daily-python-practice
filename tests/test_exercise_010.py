import importlib
import sys

import pytest

import exercises.beverage as _bev_mod
from exercises.beverage import DarkRoast, Decaf, Espresso, HouseBlend

"""Ensure condiment_decorator can import the Beverage base when it does a top-level
import operation.
The source files live under src/exercises; tests run with src on sys.path in this
project, so we load the package module and insert it as the top-level name 'beverage'
expected by the file."""

sys.modules["beverage"] = _bev_mod

condiment_mod = importlib.import_module("exercises.condiment_decorator")


def test_basic_beverage_properties():
    e = Espresso()
    assert e.get_description() == "Espresso"
    assert e.cost() == pytest.approx(1.99)


def test_single_condiment_adds_description_and_cost():
    base = Espresso()
    decorated = condiment_mod.Milk(base)
    assert decorated.get_description().startswith("Espresso")
    assert decorated.get_description().endswith(" + Milk")
    assert decorated.cost() == pytest.approx(base.cost() + 0.10)


def test_multiple_condiments_and_ordering_in_description():
    hb = HouseBlend()
    decorated = condiment_mod.Mocha(condiment_mod.Soy(condiment_mod.Whip(hb)))
    desc = decorated.get_description()
    # Expect base description then each condiment in the wrapping order
    assert desc == "House Blend Coffee + Whip + Soy + Mocha"
    expected_cost = hb.cost() + 0.1 + 0.15 + 0.2
    assert decorated.cost() == pytest.approx(expected_cost)


def test_all_condiments_on_one_beverage_cost():
    dr = DarkRoast()
    fully_loaded = condiment_mod.Milk(
        condiment_mod.Mocha(condiment_mod.Soy(condiment_mod.Whip(dr)))
    )
    expected = dr.cost() + 0.1 + 0.2 + 0.15 + 0.1
    assert fully_loaded.cost() == pytest.approx(expected)
    # verify description contains each condiment once
    for name in ("Milk", "Mocha", "Soy", "Whip"):
        assert f" + {name}" in fully_loaded.get_description()


def test_decoration_order_does_not_change_total_cost():
    d = Decaf()
    order1 = condiment_mod.Milk(condiment_mod.Mocha(d))
    order2 = condiment_mod.Mocha(condiment_mod.Milk(d))
    assert order1.cost() == pytest.approx(order2.cost())
    assert order1.cost() == pytest.approx(d.cost() + 0.1 + 0.2)


def test_double_condiment_and_description_repetition():
    e = Espresso()
    double_mocha = condiment_mod.Mocha(condiment_mod.Mocha(e))
    assert double_mocha.cost() == pytest.approx(e.cost() + 0.2 + 0.2)
    # description should show Mocha twice
    assert double_mocha.get_description().count(" + Mocha") == 2


@pytest.mark.parametrize(
    "cond_name, constructor, extra",
    [
        ("Milk", condiment_mod.Milk, 0.10),
        ("Mocha", condiment_mod.Mocha, 0.20),
        ("Soy", condiment_mod.Soy, 0.15),
        ("Whip", condiment_mod.Whip, 0.10),
    ],
)
def test_individual_condiment_additional_cost(cond_name, constructor, extra):
    base = Espresso()
    decorated = constructor(base)
    assert decorated.cost() == pytest.approx(base.cost() + extra)


def test_nested_decorations_count_and_cost():
    hb = HouseBlend()
    # 5-layer nesting
    decorated = condiment_mod.Whip(
        condiment_mod.Soy(
            condiment_mod.Mocha(condiment_mod.Milk(condiment_mod.Whip(hb)))
        )
    )
    desc = decorated.get_description()
    # there are 5 " + " separators when 5 condiments are present
    assert desc.count(" + ") == 5
    # compute expected total
    expected_total = hb.cost() + 0.1 + 0.15 + 0.2 + 0.1 + 0.1
    assert decorated.cost() == pytest.approx(expected_total)


def test_cost_breakdown_step_by_step():
    dr = DarkRoast()
    assert dr.cost() == pytest.approx(0.99)
    with_soy = condiment_mod.Soy(dr)
    assert with_soy.cost() == pytest.approx(dr.cost() + 0.15)
    with_mocha = condiment_mod.Mocha(with_soy)
    assert with_mocha.cost() == pytest.approx(dr.cost() + 0.15 + 0.2)
    with_whip = condiment_mod.Whip(with_mocha)
    assert with_whip.cost() == pytest.approx(dr.cost() + 0.15 + 0.2 + 0.1)


def test_beverage_comparison_same_condiments_across_bases():
    bases = [Espresso(), HouseBlend(), DarkRoast(), Decaf()]
    for base in bases:
        decorated = condiment_mod.Milk(condiment_mod.Mocha(base))
        assert decorated.cost() == pytest.approx(base.cost() + 0.2 + 0.1)
