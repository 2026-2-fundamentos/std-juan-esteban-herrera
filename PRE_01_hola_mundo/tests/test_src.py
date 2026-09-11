from ..src.pregunta_01 import pregunta_01
from ..src.pregunta_02 import pregunta_02


def test_01():
    """Test 01"""
    assert pregunta_01() == "Hola mundo cruel!"


def test_02():
    """Test 02"""
    assert pregunta_02() == "Hello cruel world!"
