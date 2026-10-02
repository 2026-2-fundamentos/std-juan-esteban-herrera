from pathlib import Path


def test_01():
    assert Path("submission/cluster_profiles.csv").is_file()
    assert Path("submission/cluster_sizes.csv").is_file()
    assert Path("submission/gender_profiles.csv").is_file()
    assert Path("submission/gradyear_profiles.csv").is_file()
    assert Path("submission/segmented.csv").is_file()
    assert Path("submission/top_interests.csv").is_file()
