

def test_01():
    """Test 01"""
    from ..src.pregunta_01 import pregunta_01

    assert pregunta_01() == "Hola mundo cruel!"


def test_02():
    """Test 02"""
    from ..src.pregunta_02 import pregunta_02

    assert pregunta_02() == "Hello cruel world!"
