import pytest

@pytest.fixture
def api_connection():
    from prevedere import Api
    API_KEY = "0a176139cf0c4d2585c02352285112ec"
    return Api(API_KEY)

def test_providers(api_connection):
    prov = api_connection.providers()
    assert any([True for provider in prov if provider['Name'] == "Prevedere"])

def test_search(api_connection):
    results = api_connection.search('TRFVOLUSM227NFWA')['Results']
    assert any([True for result in results if result['Name'] == "Vehicle Miles Traveled"])