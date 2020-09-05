import pytest


@pytest.mark.parametrize("param", [
    ('/recipients/', 200),
    ('/recipients/2/', 200),
    ('/recipients/220/', 404),
    ('/product-sets/', 200),
    ('/product-sets/3/', 200),
    ('/product-sets/220/', 404),
    ('/product-sets/?min_weight=2000&min_price=1000', 200),
], ids=[
    "/recipients/",
    "/recipients/2/",
    "/recipients/220/",
    "/product-sets/",
    "/product-sets/3/",
    "/product-sets/220/",
    "/product-sets/?min_weight=2000&min_price=1000'"
])
def test_simple_endpoint_check(param, client):
    response = client.get(param[0])
    assert response.status_code == param[1]
