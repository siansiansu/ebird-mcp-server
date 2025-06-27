
import pytest
from unittest.mock import AsyncMock, patch
from server import (
    ebird_get_recent_observations,
    ebird_get_hotspots,
    ebird_get_checklist_details,
    format_observations,
    format_hotspots,
    format_checklist
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

