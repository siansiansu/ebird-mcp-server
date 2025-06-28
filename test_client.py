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

@pytest.mark.asyncio
@respx.mock
async def test_get_nearest_observations_for_species(client):
    """Test getting nearest observations for a species."""
    lat, lng, species_code = 40.7128, -74.0060, "norcar"
    mock_response = [{"comName": "Northern Cardinal"}]
    
    respx.get(f"{BASE_URL}/data/nearest/geo/recent/{species_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_nearest_observations_for_species(lat, lng, species_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_historic_observations(client):
    """Test getting historic observations."""
    region_code, year, month, day = "US-NY", 2023, 10, 26
    mock_response = [{"comName": "American Robin"}]
    
    respx.get(f"{BASE_URL}/data/obs/{region_code}/historic/{year}/{month}/{day}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_historic_observations(region_code, year, month, day)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_top100(client):
    """Test getting top 100 observations."""
    region_code, year, month, day = "US-NY", 2023, 10, 26
    mock_response = [{"comName": "Blue Jay"}]
    
    respx.get(f"{BASE_URL}/product/top100/{region_code}/{year}/{month}/{day}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_top100(region_code, year, month, day)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_recent_checklists_feed(client):
    """Test getting recent checklists feed."""
    region_code = "US-NY"
    mock_response = [{"subId": "S123"}]
    
    respx.get(f"{BASE_URL}/product/lists/{region_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_recent_checklists_feed(region_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_checklist_feed_on_date(client):
    """Test getting checklist feed on a specific date."""
    region_code, year, month, day = "US-NY", 2023, 10, 26
    mock_response = [{"subId": "S456"}]
    
    respx.get(f"{BASE_URL}/product/lists/{region_code}/{year}/{month}/{day}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_checklist_feed_on_date(region_code, year, month, day)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_regional_statistics_on_date(client):
    """Test getting regional statistics on a specific date."""
    region_code, year, month, day = "US-NY", 2023, 10, 26
    mock_response = {"numSpecies": 100}
    
    respx.get(f"{BASE_URL}/product/stats/{region_code}/{year}/{month}/{day}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_regional_statistics_on_date(region_code, year, month, day)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_species_list_for_region(client):
    """Test getting species list for a region."""
    region_code = "US-NY"
    mock_response = [{"speciesCode": "norcar"}]
    
    respx.get(f"{BASE_URL}/product/spplist/{region_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_species_list_for_region(region_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_adjacent_regions(client):
    """Test getting adjacent regions."""
    region_code = "US-NY"
    mock_response = [{"code": "US-NJ"}]
    
    respx.get(f"{BASE_URL}/ref/adjacent/{region_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_adjacent_regions(region_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_hotspot_info(client):
    """Test getting hotspot info."""
    loc_id = "L123"
    mock_response = {"locId": loc_id, "locName": "Central Park"}
    
    respx.get(f"{BASE_URL}/ref/hotspot/info/{loc_id}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_hotspot_info(loc_id)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_taxa_locale_codes(client):
    """Test getting taxa locale codes."""
    mock_response = [{"code": "en"}]
    
    respx.get(f"{BASE_URL}/ref/taxa-locales/ebird").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_taxa_locale_codes()
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_taxonomy_versions(client):
    """Test getting taxonomy versions."""
    mock_response = [{"version": "2023"}]
    
    respx.get(f"{BASE_URL}/ref/taxonomy/versions").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_taxonomy_versions()
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_taxonomic_groups(client):
    """Test getting taxonomic groups."""
    species_grouping = "birds"
    mock_response = [{"group": "birds"}]
    
    respx.get(f"{BASE_URL}/ref/sppgroup/{species_grouping}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_taxonomic_groups(species_grouping)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_region_info(client):
    """Test getting region info."""
    region_code = "US-NY"
    mock_response = {"code": region_code, "name": "New York"}
    
    respx.get(f"{BASE_URL}/ref/region/info/{region_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_region_info(region_code)
    assert response == mock_response

@pytest.mark.asyncio
@respx.mock
async def test_get_sub_region_list(client):
    """Test getting sub region list."""
    region_type, parent_region_code = "state", "US"
    mock_response = [{"code": "US-NY"}]
    
    respx.get(f"{BASE_URL}/ref/region/list/{region_type}/{parent_region_code}").mock(return_value=Response(200, json=mock_response))
    
    response = await client.get_sub_region_list(region_type, parent_region_code)
    assert response == mock_response