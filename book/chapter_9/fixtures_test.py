import pytest
from fixtures import Address, Person

@pytest.fixture
def address():
    return Address(
        street_no="1",
        postal_code="5000",
        city="Hyderabad",
        country="India"
    )

@pytest.fixture
def person(address):
    return Person(name="Nia",
                  age=21,
                  gender="male",
                  address=address)

def test_address(person):
    assert person.address.country == "India"

def test_age(person):
    assert person.age == 21

def test_postal_code(person):
    assert person.address.postal_code == "5000"