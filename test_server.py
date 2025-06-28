import pytest
from unittest.mock import AsyncMock, patch
from server import (
    ebird_get_recent_observations,
    ebird_get_hotspots,
    ebird_get_checklist_details,
    format_observations,
    format_hotspots,
    format_checklist,
    ebird_get_nearest_observations_for_species,
    ebird_get_historic_observations,
    ebird_get_top100,
    ebird_get_recent_checklists_feed,
    ebird_get_checklist_feed_on_date,
    ebird_get_regional_statistics_on_date,
    ebird_get_species_list_for_region,
    ebird_get_adjacent_regions,
    ebird_get_hotspot_info,
    ebird_get_taxa_locale_codes,
    ebird_get_taxonomy_versions,
    ebird_get_taxonomic_groups,
    ebird_get_region_info,
    ebird_get_sub_region_list
)

@pytest.fixture
def mock_ebird_client():
    """Fixture to mock the EBirdClient."""
    with patch('server.ebird', new_callable=AsyncMock) as mock_client:
        yield mock_client

@pytest.mark.asyncio
async def test_ebird_get_recent_observations_tool(mock_ebird_client):
    """Test the ebird_get_recent_observations MCP tool."""
    mock_ebird_client.get_recent_observations.return_value = [
        {
            "comName": "Northern Cardinal",
            "sciName": "Cardinalis cardinalis",
            "locName": "Central Park",
            "obsDt": "2023-10-27 10:00",
            "howMany": 2
        }
    ]
    
    result = await ebird_get_recent_observations(regionCode="US-NY")
    
    assert "content" in result
    assert "text" in result["content"][0]
    assert "Northern Cardinal" in result["content"][0]["text"]
    mock_ebird_client.get_recent_observations.assert_called_once_with("US-NY", {})

@pytest.mark.asyncio
async def test_ebird_get_hotspots_tool(mock_ebird_client):
    """Test the ebird_get_hotspots MCP tool."""
    mock_ebird_client.get_hotspots.return_value = [
        {"locId": "L123", "locName": "Central Park", "lat": 40.7, "lng": -73.9}
    ]
    
    result = await ebird_get_hotspots(regionCode="US-NY")
    
    assert "Central Park" in result["content"][0]["text"]
    mock_ebird_client.get_hotspots.assert_called_once_with("US-NY", {})


def test_format_observations_empty():
    """Test formatting with no observations."""
    assert format_observations([]) == "No observations found."


def test_format_hotspots_single():
    """Test formatting a single hotspot."""
    hotspot = [{"locId": "L456", "locName": "Bryant Park"}]
    formatted = format_hotspots(hotspot)
    assert "Bryant Park" in formatted
    assert "L456" in formatted

@pytest.mark.asyncio
async def test_ebird_get_checklist_tool(mock_ebird_client):
    """Test the ebird_get_checklist_details MCP tool."""
    checklist_id = "S12345678"
    mock_checklist = {
        "subId": checklist_id,
        "loc": {"locName": "Prospect Park"},
        "obsDt": "2023-10-28",
        "userDisplayName": "Test User",
        "obs": [
            {"comName": "American Robin", "sciName": "Turdus migratorius", "howMany": 5}
        ]
    }
    mock_ebird_client.get_checklist.return_value = mock_checklist
    
    result = await ebird_get_checklist_details(checklistId=checklist_id)
    
    assert "Prospect Park" in result["content"][0]["text"]
    assert "American Robin" in result["content"][0]["text"]
    mock_ebird_client.get_checklist.assert_called_once_with(checklist_id)

def test_format_checklist():
    """Test formatting a checklist."""
    checklist = {
        "subId": "S98765",
        "loc": {"locName": "Green-Wood Cemetery"},
        "obsDt": "2023-10-29",
        "userDisplayName": "Another User",
        "obs": [
            {"comName": "Blue Jay", "sciName": "Cyanocitta cristata", "howMany": 3},
            {"comName": "Dark-eyed Junco", "sciName": "Junco hyemalis", "howMany": 10}
        ]
    }
    formatted = format_checklist(checklist)
    assert "S98765" in formatted
    assert "Green-Wood Cemetery" in formatted
    assert "Blue Jay" in formatted
    assert "Count: 10" in formatted

@pytest.mark.asyncio
async def test_ebird_get_nearest_observations_for_species_tool(mock_ebird_client):
    """Test the ebird_get_nearest_observations_for_species MCP tool."""
    mock_ebird_client.get_nearest_observations_for_species.return_value = [
        {"comName": "House Sparrow", "locName": "NYC"}
    ]
    result = await ebird_get_nearest_observations_for_species(lat=40.0, lng=-70.0, speciesCode="houspa")
    assert "House Sparrow" in result["content"][0]["text"]
    mock_ebird_client.get_nearest_observations_for_species.assert_called_once_with(40.0, -70.0, "houspa", {})

@pytest.mark.asyncio
async def test_ebird_get_historic_observations_tool(mock_ebird_client):
    """Test the ebird_get_historic_observations MCP tool."""
    mock_ebird_client.get_historic_observations.return_value = [
        {"comName": "American Crow", "locName": "Albany"}
    ]
    result = await ebird_get_historic_observations(regionCode="US-NY", year=2023, month=1, day=1)
    assert "American Crow" in result["content"][0]["text"]
    mock_ebird_client.get_historic_observations.assert_called_once_with("US-NY", 2023, 1, 1, {})

@pytest.mark.asyncio
async def test_ebird_get_top100_tool(mock_ebird_client):
    """Test the ebird_get_top100 MCP tool."""
    mock_ebird_client.get_top100.return_value = [
        {"comName": "Bald Eagle", "locName": "Upstate NY"}
    ]
    result = await ebird_get_top100(regionCode="US-NY", year=2023, month=1, day=1)
    assert "Bald Eagle" in result["content"][0]["text"]
    mock_ebird_client.get_top100.assert_called_once_with("US-NY", 2023, 1, 1)

@pytest.mark.asyncio
async def test_ebird_get_recent_checklists_feed_tool(mock_ebird_client):
    """Test the ebird_get_recent_checklists_feed MCP tool."""
    mock_ebird_client.get_recent_checklists_feed.return_value = [
        {"subId": "S12345", "locName": "Central Park"}
    ]
    result = await ebird_get_recent_checklists_feed(regionCode="US-NY")
    assert "S12345" in result["content"][0]["text"]
    mock_ebird_client.get_recent_checklists_feed.assert_called_once_with("US-NY")

@pytest.mark.asyncio
async def test_ebird_get_checklist_feed_on_date_tool(mock_ebird_client):
    """Test the ebird_get_checklist_feed_on_date MCP tool."""
    mock_ebird_client.get_checklist_feed_on_date.return_value = [
        {"subId": "S67890", "locName": "Prospect Park"}
    ]
    result = await ebird_get_checklist_feed_on_date(regionCode="US-NY", year=2023, month=1, day=1)
    assert "S67890" in result["content"][0]["text"]
    mock_ebird_client.get_checklist_feed_on_date.assert_called_once_with("US-NY", 2023, 1, 1)

@pytest.mark.asyncio
async def test_ebird_get_regional_statistics_on_date_tool(mock_ebird_client):
    """Test the ebird_get_regional_statistics_on_date MCP tool."""
    mock_ebird_client.get_regional_statistics_on_date.return_value = {"numSpecies": 150}
    result = await ebird_get_regional_statistics_on_date(regionCode="US-NY", year=2023, month=1, day=1)
    assert "150" in result["content"][0]["text"]
    mock_ebird_client.get_regional_statistics_on_date.assert_called_once_with("US-NY", 2023, 1, 1)

@pytest.mark.asyncio
async def test_ebird_get_species_list_for_region_tool(mock_ebird_client):
    """Test the ebird_get_species_list_for_region MCP tool."""
    mock_ebird_client.get_species_list_for_region.return_value = [
        {"speciesCode": "norcar", "comName": "Northern Cardinal", "sciName": "Cardinalis cardinalis"}
    ]
    result = await ebird_get_species_list_for_region(regionCode="US-NY")
    assert "Northern Cardinal" in result["content"][0]["text"]
    mock_ebird_client.get_species_list_for_region.assert_called_once_with("US-NY")

@pytest.mark.asyncio
async def test_ebird_get_adjacent_regions_tool(mock_ebird_client):
    """Test the ebird_get_adjacent_regions MCP tool."""
    mock_ebird_client.get_adjacent_regions.return_value = [
        {"code": "US-NJ", "name": "New Jersey"}
    ]
    result = await ebird_get_adjacent_regions(regionCode="US-NY")
    assert "US-NJ" in result["content"][0]["text"]
    mock_ebird_client.get_adjacent_regions.assert_called_once_with("US-NY")

@pytest.mark.asyncio
async def test_ebird_get_hotspot_info_tool(mock_ebird_client):
    """Test the ebird_get_hotspot_info MCP tool."""
    mock_ebird_client.get_hotspot_info.return_value = {"locId": "L123", "locName": "Central Park"}
    result = await ebird_get_hotspot_info(locId="L123")
    assert "Central Park" in result["content"][0]["text"]
    mock_ebird_client.get_hotspot_info.assert_called_once_with("L123")

@pytest.mark.asyncio
async def test_ebird_get_taxa_locale_codes_tool(mock_ebird_client):
    """Test the ebird_get_taxa_locale_codes MCP tool."""
    mock_ebird_client.get_taxa_locale_codes.return_value = [
        {"code": "en", "name": "English"}
    ]
    result = await ebird_get_taxa_locale_codes()
    assert "en" in result["content"][0]["text"]
    mock_ebird_client.get_taxa_locale_codes.assert_called_once_with()

@pytest.mark.asyncio
async def test_ebird_get_taxonomy_versions_tool(mock_ebird_client):
    """Test the ebird_get_taxonomy_versions MCP tool."""
    mock_ebird_client.get_taxonomy_versions.return_value = [
        {"version": "2023", "date": "2023-01-01"}
    ]
    result = await ebird_get_taxonomy_versions()
    assert "2023" in result["content"][0]["text"]
    mock_ebird_client.get_taxonomy_versions.assert_called_once_with()

@pytest.mark.asyncio
async def test_ebird_get_taxonomic_groups_tool(mock_ebird_client):
    """Test the ebird_get_taxonomic_groups MCP tool."""
    mock_ebird_client.get_taxonomic_groups.return_value = [
        {"groupName": "birds", "groupCode": "birds", "description": "All birds"}
    ]
    result = await ebird_get_taxonomic_groups(speciesGrouping="birds")
    assert "birds" in result["content"][0]["text"]
    mock_ebird_client.get_taxonomic_groups.assert_called_once_with("birds")

@pytest.mark.asyncio
async def test_ebird_get_region_info_tool(mock_ebird_client):
    """Test the ebird_get_region_info MCP tool."""
    mock_ebird_client.get_region_info.return_value = {"code": "US-NY", "name": "New York"}
    result = await ebird_get_region_info(regionCode="US-NY")
    assert "New York" in result["content"][0]["text"]
    mock_ebird_client.get_region_info.assert_called_once_with("US-NY")

@pytest.mark.asyncio
async def test_ebird_get_sub_region_list_tool(mock_ebird_client):
    """Test the ebird_get_sub_region_list MCP tool."""
    mock_ebird_client.get_sub_region_list.return_value = [
        {"code": "US-NY", "name": "New York"}
    ]
    result = await ebird_get_sub_region_list(regionType="state", parentRegionCode="US")
    assert "US-NY" in result["content"][0]["text"]
    mock_ebird_client.get_sub_region_list.assert_called_once_with("state", "US")