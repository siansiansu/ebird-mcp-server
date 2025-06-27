import os
import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from client import EBirdClient

# --- Configuration ---

mcp = FastMCP(name="ebird-api", version="1.0.0")

EBIRD_API_KEY = os.getenv("EBIRD_API_KEY", "EBIRD_API_KEY")
if EBIRD_API_KEY == "EBIRD_API_KEY":
    print("Using default eBird API key. Please replace with your own key and set it as an environment variable.", file=sys.stderr)

ebird = EBirdClient(EBIRD_API_KEY)

DEBUG = os.getenv("DEBUG", "true").lower() == "true"


def log(*args: Any):
    """Simple logger for debugging."""
    if DEBUG:
        print("[DEBUG]", *args, file=sys.stderr)

def format_observations(observations: List[Dict]) -> str:
    """Formats a list of observation dictionaries into a readable string."""
    if not observations:
        return "No observations found."
    lines = []
    for obs in observations:
        how_many = f"Count: {obs.get('howMany')}" if obs.get("howMany") else "Present"
        date = obs.get("obsDt", "Unknown date")
        time = obs.get("obsTime", "")
        datetime_str = f"{date} {time}".strip()
        line = (
            f"Species: {obs.get('comName')} ({obs.get('sciName')})\n"
            f"Location: {obs.get('locName')}\n"
            f"{how_many}\n"
            f"Date: {datetime_str}\n"
            f"Coordinates: {obs.get('lat')}, {obs.get('lng')}"
        )
        if obs.get("userDisplayName"):
            line += f"\nObserver: {obs.get('userDisplayName')}"
        lines.append(line)
    return "\n\n".join(lines)


def format_hotspots(hotspots: List[Dict]) -> str:
    """Formats a list of hotspot dictionaries into a readable string."""
    if not hotspots:
        return "No hotspots found."
    lines = []
    for hs in hotspots:
        name = hs.get("locName", f"Hotspot {hs.get('locId', 'Unknown')}")
        coords = f"{hs.get('lat')}, {hs.get('lng')}" if hs.get("lat") and hs.get("lng") else "Not available"
        species = hs.get("numSpecies", "Unknown")
        lines.append(
            f"Hotspot: {name}\n"
            f"Location ID: {hs.get('locId')}\n"
            f"Coordinates: {coords}\n"
            f"Number of Species: {species}"
        )
    return "\n\n".join(lines)


def format_taxonomy(taxa: List[Dict]) -> str:
    """Formats taxonomy data into a readable string."""
    if not taxa:
        return "No taxonomy data found."
    lines = []
    for taxon in taxa:
        lines.append(
            f"Common Name: {taxon.get('comName')}\n"
            f"Scientific Name: {taxon.get('sciName')}\n"
            f"Species Code: {taxon.get('speciesCode')}\n"
            f"Category: {taxon.get('category')}"
        )
    return "\n\n".join(lines)


def format_taxonomy_forms(forms: List[str]) -> str:
    """Formats taxonomy forms into a readable string."""
    if not forms:
        return "No taxonomy forms found."
    return "Taxonomy Forms:\n" + "\n".join(f"- {form}" for form in forms)

def format_checklist(checklist: Dict) -> str:
    """Formats a checklist dictionary into a readable string."""
    if not checklist:
        return "Checklist not found."

    lines = [
        f"Checklist ID: {checklist.get('subId')}",
        f"Location: {checklist.get('loc', {}).get('locName')}",
        f"Date: {checklist.get('obsDt')}",
        f"Observer: {checklist.get('userDisplayName')}",
        "---",
        "Observations:"
    ]

    for obs in checklist.get("obs", []):
        how_many = f"Count: {obs.get('howMany')}" if obs.get("howMany") else "Present"
        lines.append(
            f"  - {obs.get('comName')} ({obs.get('sciName')}) - {how_many}"
        )
    
    return "\n".join(lines)


# --- MCP Tools ---

@mcp.tool(
    name="ebird_get_recent_observations",
    description="Get recent bird observations in a region.",
)
async def ebird_get_recent_observations(
    regionCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
    hotspot: Optional[bool] = None,
    detail: Optional[str] = None,
) -> Dict:
    """Get recent bird observations in a region.

    :param regionCode: The regional code (e.g., US-NY).
    :param back: The number of days back to fetch observations (1-30).
    :param maxResults: Maximum number of results to return.
    :param includeProvisional: Include observations not yet reviewed.
    :param hotspot: Only fetch observations from hotspots.
    :param detail: Level of detail for observations. Can be 'simple' or 'full'.
    """
    log(f"Received ebird_get_recent_observations request for region: {regionCode}")
    options = {
        "back": back,
        "maxResults": maxResults,
        "includeProvisional": includeProvisional,
        "hotspot": hotspot,
        "detail": detail,
    }
    # Filter out None values from options
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_recent_observations(regionCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_recent_observations_for_species",
    description="Get recent observations of a specific species in a region.",
)
async def ebird_get_recent_observations_for_species(
    regionCode: str,
    speciesCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
    hotspot: Optional[bool] = None,
) -> Dict:
    """Get recent observations of a specific species in a region.

    :param regionCode: The regional code.
    :param speciesCode: The eBird code for the species.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    :param hotspot: Only from hotspots.
    """
    log(f"Received ebird_get_recent_observations_for_species request for region: {regionCode}, species: {speciesCode}")
    options = {
        "back": back,
        "maxResults": maxResults,
        "includeProvisional": includeProvisional,
        "hotspot": hotspot,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_recent_observations_for_species(regionCode, speciesCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_notable_observations",
    description="Get recent notable (unusual) observations in a region.",
)
async def ebird_get_notable_observations(
    regionCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    detail: Optional[str] = None,
) -> Dict:
    """Get recent notable (unusual) observations in a region.

    :param regionCode: The regional code.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param detail: Level of detail. Can be 'simple' or 'full'.
    """
    log(f"Received ebird_get_notable_observations request for region: {regionCode}")
    options = {
        "back": back,
        "maxResults": maxResults,
        "detail": detail,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_notable_observations(regionCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_observations",
    description="Get bird observations near a specific latitude and longitude.",
)
async def ebird_get_nearby_observations(
    lat: float,
    lng: float,
    dist: Optional[int] = None,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
    hotspot: Optional[bool] = None,
) -> Dict:
    """Get bird observations near a specific latitude and longitude.

    :param lat: Latitude.
    :param lng: Longitude.
    :param dist: Distance in kilometers (0-50).
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    :param hotspot: Only from hotspots.
    """
    log(f"Received ebird_get_nearby_observations request for lat: {lat}, lng: {lng}")
    options = {
        "dist": dist,
        "back": back,
        "maxResults": maxResults,
        "includeProvisional": includeProvisional,
        "hotspot": hotspot,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_nearby_observations(lat, lng, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_notable_observations",
    description="Get notable observations near a specific location.",
)
async def ebird_get_nearby_notable_observations(
    lat: float,
    lng: float,
    dist: Optional[int] = None,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
) -> Dict:
    """Get notable observations near a specific location.

    :param lat: Latitude.
    :param lng: Longitude.
    :param dist: Distance in kilometers.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    """
    log(f"Received ebird_get_nearby_notable_observations request for lat: {lat}, lng: {lng}")
    options = {
        "dist": dist,
        "back": back,
        "maxResults": maxResults,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_nearby_notable_observations(lat, lng, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_observations_for_species",
    description="Get observations of a species near a specific location.",
)
async def ebird_get_nearby_observations_for_species(
    lat: float,
    lng: float,
    speciesCode: str,
    dist: Optional[int] = None,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
) -> Dict:
    """Get observations of a species near a specific location.

    :param lat: Latitude.
    :param lng: Longitude.
    :param speciesCode: The eBird code for the species.
    :param dist: Distance in kilometers.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    """
    log(f"Received ebird_get_nearby_observations_for_species request for lat: {lat}, lng: {lng}, species: {speciesCode}")
    options = {
        "dist": dist,
        "back": back,
        "maxResults": maxResults,
        "includeProvisional": includeProvisional,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_nearby_observations_for_species(lat, lng, speciesCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_hotspots",
    description="Get the list of birding hotspots in a region.",
)
async def ebird_get_hotspots(
    regionCode: str,
    back: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
) -> Dict:
    """Get the list of birding hotspots in a region.

    :param regionCode: The regional code.
    :param back: Days back to consider for recent sightings.
    :param includeProvisional: Include provisional data.
    """
    log(f"Received ebird_get_hotspots request for region: {regionCode}")
    options = {
        "back": back,
        "includeProvisional": includeProvisional,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_hotspots(regionCode, options)
    return {"content": [{"type": "text", "text": format_hotspots(data)}]}


@mcp.tool(
    name="ebird_get_nearby_hotspots",
    description="Get birding hotspots near a specific location.",
)
async def ebird_get_nearby_hotspots(
    lat: float,
    lng: float,
    dist: Optional[int] = None,
    back: Optional[int] = None,
) -> Dict:
    """Get birding hotspots near a specific location.

    :param lat: Latitude.
    :param lng: Longitude.
    :param dist: Distance in kilometers.
    :param back: Days back to consider.
    """
    log(f"Received ebird_get_nearby_hotspots request for lat: {lat}, lng: {lng}")
    options = {
        "dist": dist,
        "back": back,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_nearby_hotspots(lat, lng, options)
    return {"content": [{"type": "text", "text": format_hotspots(data)}]}


@mcp.tool(
    name="ebird_get_taxonomy",
    description="Get the official eBird taxonomy.",
)
async def ebird_get_taxonomy(
    locale: Optional[str] = None,
    cat: Optional[str] = None,
    fmt: Optional[str] = None,
) -> Dict:
    """Get the official eBird taxonomy.

    :param locale: Language for common names.
    :param cat: Taxonomic category.
    :param fmt: Format (json or csv).
    """
    log(f"Received ebird_get_taxonomy request with args: locale={locale}, cat={cat}, fmt={fmt}")
    options = {
        "locale": locale,
        "cat": cat,
        "fmt": fmt,
    }
    options = {k: v for k, v in options.items() if v is not None}
    data = await ebird.get_taxonomy(options)
    return {"content": [{"type": "text", "text": format_taxonomy(data)}]}


@mcp.tool(
    name="ebird_get_taxonomy_forms",
    description="Get all identifiable forms (subspecies, etc.) for a species.",
)
async def ebird_get_taxonomy_forms(
    speciesCode: str,
) -> Dict:
    """Get all identifiable forms (subspecies, etc.) for a species.

    :param speciesCode: The eBird code for the species.
    """
    log(f"Received ebird_get_taxonomy_forms request for species: {speciesCode}")
    data = await ebird.get_taxonomy_forms(speciesCode)
    return {"content": [{"type": "text", "text": format_taxonomy_forms(data)}]}

@mcp.tool(
    name="ebird_get_checklist_details",
    description="Get the details of a specific eBird checklist.",
)
async def ebird_get_checklist_details(
    checklistId: str,
) -> Dict:
    """Get the details of a specific eBird checklist.

    :param checklistId: The ID of the checklist (e.g., S12345678).
    """
    log(f"Received ebird_get_checklist_details request for checklist: {checklistId}")
    data = await ebird.get_checklist(checklistId)
    return {"content": [{"type": "text", "text": format_checklist(data)}]}


if __name__ == "__main__":
    mcp.run()
