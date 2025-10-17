from add import add

def test_add():
    assert add(2,3) == 5

def test_two():
    assert add(10000, 1) == 10001