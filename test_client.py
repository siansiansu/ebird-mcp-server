
import pytest
import respx
from httpx import Response
from client import EBirdClient

BASE_URL = 'https://api.ebird.org/v2'

@pytest.fixture
def client():
    """Fixture to create an EBirdClient instance."""
    return EBirdClient(api_key="test_key")

@pytest.mark.asyncio
@respx.mock
async def test_get_recent_observations(client):
    """Test getting recent observations."""
    region_code = "US-NY"
    mock_response = [{"speciesCode": "norcar", "comName": "Northern Cardinal"}]
    
    respx.get(f"{BASE_URL}/data/obs/{region_code}/recent").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_recent_observations(region_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_recent_observations_for_species(client):
    """Test getting recent observations for a species."""
    region_code = "US-NY"
    species_code = "norcar"
    mock_response = [{"locId": "L12345"}]
    
    respx.get(f"{BASE_URL}/data/obs/{region_code}/recent/{species_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_recent_observations_for_species(region_code, species_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_nearby_hotspots_json(client):
    """Test getting nearby hotspots with a JSON response."""
    lat, lng = 40.7128, -74.0060
    mock_response = [{"locId": "L123", "locName": "Central Park"}]
    
    respx.get(f"{BASE_URL}/ref/hotspot/geo").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_nearby_hotspots(lat, lng)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_nearby_hotspots_fallback(client):
    """Test fallback mechanism for getting nearby hotspots."""
    lat, lng = 40.7128, -74.0060
    
    # First request for JSON fails, second for text succeeds
    respx.get(f"{BASE_URL}/ref/hotspot/geo", params={'fmt': 'json'}).mock(side_effect=Response(500))
    respx.get(f"{BASE_URL}/ref/hotspot/geo").mock(return_value=Response(200, text="L123, L456"))
    
    response = await client.get_nearby_hotspots(lat, lng)
    assert len(response) == 2
    assert response[0]['locId'] == 'L123'
    assert response[1]['locName'] == 'Hotspot L456'

@pytest.mark.asyncio
@respx.mock
async def test_make_request_handles_boolean_params(client):
    """Test that make_request correctly handles boolean parameters."""
    endpoint = "/data/obs/US-NY/recent"
    route = respx.get(f"{BASE_URL}{endpoint}").mock(return_value=Response(200, json={}))
    
    await client.make_request(endpoint, params={'hotspot': True, 'includeProvisional': False})
    
    assert route.called
    called_url = route.calls.last.request.url
    assert "hotspot=true" in str(called_url)
    assert "includeProvisional=false" in str(called_url)

@pytest.mark.asyncio
@respx.mock
async def test_get_checklist(client):
    """Test getting a checklist."""
    checklist_id = "S12345678"
    mock_response = {"subId": checklist_id, "obs": []}
    
    respx.get(f"{BASE_URL}/product/checklist/view/{checklist_id}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_checklist(checklist_id)
    assert response == mock_response

