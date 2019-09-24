import pytest
from vulncat import vulncat

url="http://www.google.com"

def test_order_soup():
    soup = app.order_soup(url)

    assert soup is not None