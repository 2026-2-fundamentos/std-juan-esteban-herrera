import os

FOLDER = "PRE_02_air_france_447"
OUTPUT_FOLDER = f"{FOLDER}/submission"


def test_01():

    assert os.path.exists(f"{OUTPUT_FOLDER}/search_plan.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/plan_comparison.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/search_planning_map.png")
