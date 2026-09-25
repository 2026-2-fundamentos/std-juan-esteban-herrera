import pandas as pd


def test_01():
    from ..src.main import OUTPUT_FILE, main

    main()

    if not OUTPUT_FILE.exists():
        raise Exception("Output file does not exist")

    df = pd.read_csv(OUTPUT_FILE)

    supplier = df["supplier"].drop_duplicates().sort_values().tolist()
    assert len(supplier) == 20

    for value in [
        "amazon web services colombia",
        "BANCOLOMBIA S.A.",
        "Cementos Argos SA",
        "cementos argos s.a.",
        "Corona SAS",
        "GOOGLE COLOMBIA LTDA.",
        "IBM Colombia SAS.",
        "ibm colombia s.a.s.",
        "MICROSOFT COLOMBIA INC.",
        "Nutresa SA",
        "nutresa s.a.",
        "oracle colombia ltda.",
        "POSTOBÓN S.A.",
        "Postobon S.A.",
        "SAP Colombia SAS",
        "SIEMENS S.A.S.",
        "siemens s.a.s.",
    ]:
        assert value not in supplier

    assert all(
        df.country.dropna().drop_duplicates().apply(lambda x: x == "COL").to_list()
    )
