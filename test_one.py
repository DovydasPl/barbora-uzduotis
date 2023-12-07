import pytest
from name import Name


@pytest.fixture
def name():
    print('Starting')
    name = Name()
    yield name
    print('The End')


def test_temp(name):
    assert name.var == 'Barbora'
