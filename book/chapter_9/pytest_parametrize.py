import pytest 
from add import add

@pytest.mark.parametrize("a,b,result", [(1,2,3), (0, 0, 0), (1,2,2)])
def test_add(a, b, result):
    assert add(a, b) == result