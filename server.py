import os
import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from client import EBirdClient

# --- Configuration ---

mcp = FastMCP(name="ebird-api", version="1.0.0")

EBIRD_API_KEY = os.getenv("EBIRD_API_KEY", "EBIRD_API_KEY")
if EBIRD_API_KEY == "EBIRD_API_KEY":
    print(
        "Using default eBird API key. Please replace with your own key and set it as an environment variable.",
        file=sys.stderr,
    )

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
        coords = (
            f"{hs.get('lat')}, {hs.get('lng')}"
            if hs.get("lat") and hs.get("lng")
            else "Not available"
        )
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
        "Observations:",
    ]

    for obs in checklist.get("obs", []):
        how_many = f"Count: {obs.get('howMany')}" if obs.get("howMany") else "Present"
        lines.append(f"  - {obs.get('comName')} ({obs.get('sciName')}) - {how_many}")

    return "\n".join(lines)


def format_checklists(checklists: List[Dict]) -> str:
    """Formats a list of checklist dictionaries into a readable string."""
    if not checklists:
        return "No checklists found."
    formatted_checklists = [format_checklist(c) for c in checklists]
    return "\n\n---\n\n".join(formatted_checklists)


def format_regional_statistics(stats: Dict) -> str:
    """Formats regional statistics into a readable string."""
    if not stats:
        return "No regional statistics found."
    lines = [
        f"Number of Checklists: {stats.get('numChecklists', 'N/A')}",
        f"Number of Species: {stats.get('numSpecies', 'N/A')}",
        f"Number of Contributors: {stats.get('numContributors', 'N/A')}",
    ]
    return "\n".join(lines)


def format_species_list(species_list: List[Dict]) -> str:
    """Formats a list of species into a readable string."""
    if not species_list:
        return "No species found."
    lines = [f"- {s.get('comName', 'N/A')} ({s.get('sciName', 'N/A')})" for s in species_list]
    return "Species List:\n" + "\n".join(lines)


def format_regions(regions: List[Dict]) -> str:
    """Formats a list of regions into a readable string."""
    if not regions:
        return "No regions found."
    lines = [f"- {r.get('name', 'N/A')} ({r.get('code', 'N/A')})" for r in regions]
    return "Regions:\n" + "\n".join(lines)


def format_hotspot_info(hotspot_info: Dict) -> str:
    """Formats hotspot information into a readable string."""
    if not hotspot_info:
        return "No hotspot information found."
    lines = [
        f"Hotspot Name: {hotspot_info.get('locName', 'N/A')}",
        f"Location ID: {hotspot_info.get('locId', 'N/A')}",
        f"Latitude: {hotspot_info.get('lat', 'N/A')}",
        f"Longitude: {hotspot_info.get('lng', 'N/A')}",
        f"Country Code: {hotspot_info.get('countryCode', 'N/A')}",
    ]
    return "\n".join(lines)


def format_taxa_locale_codes(locale_codes: List[Dict]) -> str:
    """Formats a list of taxa locale codes into a readable string."""
    if not locale_codes:
        return "No taxa locale codes found."
    lines = [f"- {lc.get('name', 'N/A')} ({lc.get('code', 'N/A')})" for lc in locale_codes]
    return "Taxa Locale Codes:\n" + "\n".join(lines)


def format_taxonomy_versions(versions: List[Dict]) -> str:
    """Formats a list of taxonomy versions into a readable string."""
    if not versions:
        return "No taxonomy versions found."
    lines = [f"- Version: {v.get('version', 'N/A')} (Latest: {v.get('latest', 'N/A')})" for v in versions]
    return "Taxonomy Versions:\n" + "\n".join(lines)


def format_taxonomic_groups(groups: List[Dict]) -> str:
    """Formats a list of taxonomic groups into a readable string."""
    if not groups:
        return "No taxonomic groups found."
    lines = [f"- {g.get('groupName', 'N/A')} ({g.get('groupCode', 'N/A')})" for g in groups]
    return "Taxonomic Groups:\n" + "\n".join(lines)


def format_region_info(region_info: Dict) -> str:
    """Formats region information into a readable string."""
    if not region_info:
        return "No region information found."
    lines = [
        f"Region Name: {region_info.get('name', 'N/A')}",
        f"Region Code: {region_info.get('code', 'N/A')}",
        f"Parent Code: {region_info.get('parentCode', 'N/A')}",
        f"Latitude: {region_info.get('lat', 'N/A')}",
        f"Longitude: {region_info.get('lng', 'N/A')}",
    ]
    return "\n".join(lines)



# --- MCP Tools ---
# data/obs
@mcp.tool(
    name="ebird_get_recent_observations",
    description="Get the list of recent observations (up to 30 days ago) of birds seen in a country, state, county, or location. Results include only the most recent observation for each species in the region specified.",
)
async def ebird_get_recent_observations(
    regionCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
    hotspot: Optional[bool] = None,
    detail: Optional[str] = None,
) -> Dict:
    """1. Get recent observations in a region.

    :param regionCode: The regional code (e.g., US-NY).
    :param back: The number of days back to fetch observations (1-30).
    :param maxResults: Maximum number of results to return.
    :param includeProvisional: Include observations not yet reviewed.
    :param hotspot: Only fetch observations from hotspots.
    :param detail: Level of detail for observations. Can be 'simple' or 'full'.
    """
    log(f"Received ebird_get_recent_observations request for region: {regionCode}")
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["regionCode", "log"] and v is not None
    }
    data = await ebird.get_recent_observations(regionCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_notable_observations",
    description="Get the list of recent, notable observations (up to 30 days ago) of birds seen in a country, region or location.",
)
async def ebird_get_notable_observations(
    regionCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    detail: Optional[str] = None,
) -> Dict:
    """2. Get recent notable observations in a region.

    :param regionCode: The regional code.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param detail: Level of detail. Can be 'simple' or 'full'.
    """
    log(f"Received ebird_get_notable_observations request for region: {regionCode}")
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["regionCode", "log"] and v is not None
    }
    data = await ebird.get_notable_observations(regionCode, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_recent_observations_for_species",
    description="Get the recent observations, up to 30 days ago, of a particular species in a country, region or location. Results include only the most recent observation from each location in the region specified.",
)
async def ebird_get_recent_observations_for_species(
    regionCode: str,
    speciesCode: str,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
    hotspot: Optional[bool] = None,
) -> Dict:
    """3. Get recent observations of a species in a region.

    :param regionCode: The regional code.
    :param speciesCode: The eBird code for the species.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    :param hotspot: Only from hotspots.
    """
    log(
        f"Received ebird_get_recent_observations_for_species request for region: {regionCode}, species: {speciesCode}"
    )
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["regionCode", "speciesCode", "log"] and v is not None
    }
    data = await ebird.get_recent_observations_for_species(
        regionCode, speciesCode, options
    )
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_observations",
    description="Get the list of recent observations (up to 30 days ago) of birds seen at locations within a radius of up to 50 kilometers, from a given set of coordinates. Results include only the most recent observation for each species in the region specified.",
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
    """4. Get recent nearby observations.

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
        k: v
        for k, v in locals().items()
        if k not in ["lat", "lng", "log"] and v is not None
    }
    data = await ebird.get_nearby_observations(lat, lng, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_observations_for_species",
    description="Get all observations of a species, seen up to 30 days ago, at any location within a radius of up to 50 kilometers, from a given set of coordinates. Results include only the most recent observation from each location in the region specified.",
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
    """5. Get recent nearby observations of a species.

    :param lat: Latitude.
    :param lng: Longitude.
    :param speciesCode: The eBird code for the species.
    :param dist: Distance in kilometers.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    """
    log(
        f"Received ebird_get_nearby_observations_for_species request for lat: {lat}, lng: {lng}, species: {speciesCode}"
    )
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["lat", "lng", "speciesCode", "log"] and v is not None
    }
    data = await ebird.get_nearby_observations_for_species(
        lat, lng, speciesCode, options
    )
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearest_observations_for_species",
    description="Find the nearest locations where a species has been seen recently.",
)
async def ebird_get_nearest_observations_for_species(
    lat: float,
    lng: float,
    speciesCode: str,
    dist: Optional[int] = None,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
) -> Dict:
    """6. Get nearest observations of a species.

    :param lat: Latitude.
    :param lng: Longitude.
    :param speciesCode: The eBird code for the species.
    :param dist: Distance in kilometers.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    :param includeProvisional: Include provisional data.
    """
    log(
        f"Received ebird_get_nearest_observations_for_species request for lat: {lat}, lng: {lng}, species: {speciesCode}"
    )
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["lat", "lng", "speciesCode", "log"] and v is not None
    }
    data = await ebird.get_nearest_observations_for_species(
        lat, lng, speciesCode, options
    )
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_nearby_notable_observations",
    description="Get the list of notable observations (up to 30 days ago) of birds seen at locations within a radius of up to 50 kilometers, from a given set of coordinates.",
)
async def ebird_get_nearby_notable_observations(
    lat: float,
    lng: float,
    dist: Optional[int] = None,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
) -> Dict:
    """7. Get recent nearby notable observations.

    :param lat: Latitude.
    :param lng: Longitude.
    :param dist: Distance in kilometers.
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    """
    log(
        f"Received ebird_get_nearby_notable_observations request for lat: {lat}, lng: {lng}"
    )
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["lat", "lng", "log"] and v is not None
    }
    data = await ebird.get_nearby_notable_observations(lat, lng, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_historic_observations",
    description="Get a list of all taxa seen in a country, region or location on a specific date, with the specific observations determined by the rank parameter (defaults to latest observation on the date).",
)
async def ebird_get_historic_observations(
    regionCode: str,
    year: int,
    month: int,
    day: int,
    back: Optional[int] = None,
    maxResults: Optional[int] = None,
) -> Dict:
    """Get historic observations on a date.

    :param regionCode: The regional code.
    :param year: Year (e.g., 2023).
    :param month: Month (1-12).
    :param day: Day (1-31).
    :param back: Days back to fetch.
    :param maxResults: Maximum number of results.
    """
    log(
        f"Received ebird_get_historic_observations request for region: {regionCode}, date: {year}-{month}-{day}"
    )
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["regionCode", "year", "month", "day", "log"] and v is not None
    }
    data = await ebird.get_historic_observations(regionCode, year, month, day, options)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


# product
@mcp.tool(
    name="ebird_get_top100",
    description="Get the top 100 contributors on a given date for a country or region.",
)
async def ebird_get_top100(
    regionCode: str,
    year: int,
    month: int,
    day: int,
) -> Dict:
    """1. Get the top 100 contributors on a given date for a country or region.

    :param regionCode: The regional code.
    :param year: Year (e.g., 2023).
    :param month: Month (1-12).
    :param day: Day (1-31).
    """
    log(
        f"Received ebird_get_top100 request for region: {regionCode}, date: {year}-{month}-{day}"
    )
    data = await ebird.get_top100(regionCode, year, month, day)
    return {"content": [{"type": "text", "text": format_observations(data)}]}


@mcp.tool(
    name="ebird_get_recent_checklists_feed",
    description="Get information on the most recently submitted checklists for a region.",
)
async def ebird_get_recent_checklists_feed(
    regionCode: str,
) -> Dict:
    """2. Get information on the most recently submitted checklists for a region.

    :param regionCode: The regional code.
    """
    log(f"Received ebird_get_recent_checklists_feed request for region: {regionCode}")
    data = await ebird.get_recent_checklists_feed(regionCode)
    return {"content": [{"type": "text", "text": format_checklists(data)}]
}


@mcp.tool(
    name="ebird_get_checklist_feed_on_date",
    description="Get information on the checklists submitted on a given date for a country or region.",
)
async def ebird_get_checklist_feed_on_date(
    regionCode: str,
    year: int,
    month: int,
    day: int,
) -> Dict:
    """3. Get information on the checklists submitted on a given date for a country or region.

    :param regionCode: The regional code.
    :param year: Year (e.g., 2023).
    :param month: Month (1-12).
    :param day: Day (1-31).
    """
    log(
        f"Received ebird_get_checklist_feed_on_date request for region: {regionCode}, date: {year}-{month}-{day}"
    )
    data = await ebird.get_checklist_feed_on_date(regionCode, year, month, day)
    return {"content": [{"type": "text", "text": format_checklists(data)}]}


@mcp.tool(
    name="ebird_get_regional_statistics_on_date",
    description="Get a summary of the number of checklist submitted, species seen and contributors on a given date for a country or region.",
)
async def ebird_get_regional_statistics_on_date(
    regionCode: str,
    year: int,
    month: int,
    day: int,
) -> Dict:
    """4. Get a summary of the number of checklist submitted, species seen and contributors on a given date for a country or region.

    :param regionCode: The regional code.
    :param year: Year (e.g., 2023).
    :param month: Month (1-12).
    :param day: Day (1-31).
    """
    log(
        f"Received ebird_get_regional_statistics_on_date request for region: {regionCode}, date: {year}-{month}-{day}"
    )
    data = await ebird.get_regional_statistics_on_date(regionCode, year, month, day)
    return {"content": [{"type": "text", "text": format_regional_statistics(data)}]}


@mcp.tool(
    name="ebird_get_species_list_for_region",
    description="Get a list of species codes ever seen in a region, in taxonomic order (species taxa only)",
)
async def ebird_get_species_list_for_region(
    regionCode: str,
) -> Dict:
    """5. Get a list of species codes ever seen in a region, in taxonomic order (species taxa only)

    :param regionCode: The regional code.
    """
    log(f"Received ebird_get_species_list_for_region request for region: {regionCode}")
    data = await ebird.get_species_list_for_region(regionCode)
    return {"content": [{"type": "text", "text": format_species_list(data)}]}


@mcp.tool(
    name="ebird_get_checklist_details",
    description="Get the details and observations of a checklist.",
)
async def ebird_get_checklist_details(
    checklistId: str,
) -> Dict:
    """6. Get the details and observations of a checklist.

    :param checklistId: The ID of the checklist (e.g., S12345678).
    """
    log(f"Received ebird_get_checklist_details request for checklist: {checklistId}")
    data = await ebird.get_checklist(checklistId)
    return {"content": [{"type": "text", "text": format_checklist(data)}]}


# ref/geo
@mcp.tool(
    name="ebird_get_adjacent_regions",
    description="With the ref/geo end-point you can find a country's or region's neighbours.",
)
async def ebird_get_adjacent_regions(
    regionCode: str,
) -> Dict:
    """1. With the ref/geo end-point you can find a country's or region's neighbours.

    :param regionCode: The regional code.
    """
    log(f"Received ebird_get_adjacent_regions request for region: {regionCode}")
    data = await ebird.get_adjacent_regions(regionCode)
    return {"content": [{"type": "text", "text": format_regions(data)}]}


# ref/hotspot
@mcp.tool(
    name="ebird_get_hotspots",
    description="Get the list of birding hotspots in a region.",
)
async def ebird_get_hotspots(
    regionCode: str,
    back: Optional[int] = None,
    includeProvisional: Optional[bool] = None,
) -> Dict:
    """1. Get the list of birding hotspots in a region.

    :param regionCode: The regional code.
    :param back: Days back to consider for recent sightings.
    :param includeProvisional: Include provisional data.
    """
    log(f"Received ebird_get_hotspots request for region: {regionCode}")
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["regionCode", "log"] and v is not None
    }
    data = await ebird.get_hotspots(regionCode, options)
    return {"content": [{"type": "text", "text": format_hotspots(data)}]}


@mcp.tool(
    name="ebird_get_nearby_hotspots",
    description="Get the list of hotspots, within a radius of up to 50 kilometers, from a given set of coordinates.",
)
async def ebird_get_nearby_hotspots(
    lat: float,
    lng: float,
    dist: Optional[int] = None,
    back: Optional[int] = None,
) -> Dict:
    """2. Get the list of hotspots, within a radius of up to 50 kilometers, from a given set of coordinates.

    :param lat: Latitude.
    :param lng: Longitude.
    :param dist: Distance in kilometers.
    :param back: Days back to consider.
    """
    log(f"Received ebird_get_nearby_hotspots request for lat: {lat}, lng: {lng}")
    options = {
        k: v
        for k, v in locals().items()
        if k not in ["lat", "lng", "log"] and v is not None
    }
    data = await ebird.get_nearby_hotspots(lat, lng, options)
    return {"content": [{"type": "text", "text": format_hotspots(data)}]}


@mcp.tool(
    name="ebird_get_hotspot_info",
    description="Get information on the location of a hotspot.",
)
async def ebird_get_hotspot_info(
    locId: str,
) -> Dict:
    """3. Get information on the location of a hotspot.

    :param locId: The location ID of the hotspot.
    """
    log(f"Received ebird_get_hotspot_info request for hotspot: {locId}")
    data = await ebird.get_hotspot_info(locId)
    return {"content": [{"type": "text", "text": format_hotspot_info(data)}]}


# ref/taxonomy
@mcp.tool(
    name="ebird_get_taxonomy",
    description="Get the taxonomy used by eBird.",
)
async def ebird_get_taxonomy(
    locale: Optional[str] = None,
    cat: Optional[str] = None,
    fmt: Optional[str] = None,
) -> Dict:
    """1. Get the taxonomy used by eBird.

    :param locale: Language for common names.
    :param cat: Taxonomic category.
    :param fmt: Format (json or csv).
    """
    log(
        f"Received ebird_get_taxonomy request with args: locale={locale}, cat={cat}, fmt={fmt}"
    )
    options = {k: v for k, v in locals().items() if k not in ["log"] and v is not None}
    data = await ebird.get_taxonomy(options)
    return {"content": [{"type": "text", "text": format_taxonomy(data)}]}


@mcp.tool(
    name="ebird_get_taxonomy_forms",
    description="For a species, get the list of subspecies recognised in the taxonomy. The results include the species that was passed in.",
)
async def ebird_get_taxonomy_forms(
    speciesCode: str,
) -> Dict:
    """2. For a species, get the list of subspecies recognised in the taxonomy. The results include the species that was passed in.

    :param speciesCode: The eBird code for the species.
    """
    log(f"Received ebird_get_taxonomy_forms request for species: {speciesCode}")
    data = await ebird.get_taxonomy_forms(speciesCode)
    return {"content": [{"type": "text", "text": format_taxonomy_forms(data)}]}


@mcp.tool(
    name="ebird_get_taxa_locale_codes",
    description="Returns the list of supported locale codes and names for species common names, with the last time they were updated. Use the accept-language header to get translated language names when available.",
)
async def ebird_get_taxa_locale_codes() -> Dict:
    """3. Returns the list of supported locale codes and names for species common names, with the last time they were updated. Use the accept-language header to get translated language names when available."""
    log(f"Received ebird_get_taxa_locale_codes request")
    data = await ebird.get_taxa_locale_codes()
    return {"content": [{"type": "text", "text": format_taxa_locale_codes(data)}]}


@mcp.tool(
    name="ebird_get_taxonomy_versions",
    description="Returns a list of all versions of the taxonomy, with a flag indicating which is the latest.",
)
async def ebird_get_taxonomy_versions() -> Dict:
    """4. Returns a list of all versions of the taxonomy, with a flag indicating which is the latest."""
    log(f"Received ebird_get_taxonomy_versions request")
    data = await ebird.get_taxonomy_versions()
    return {"content": [{"type": "text", "text": format_taxonomy_versions(data)}]}


@mcp.tool(
    name="ebird_get_taxonomic_groups",
    description="Get the list of species groups, e.g. terns, finches, etc.",
)
async def ebird_get_taxonomic_groups(
    speciesGrouping: str,
) -> Dict:
    """5. Get the list of species groups, e.g. terns, finches, etc.

    :param speciesGrouping: The species grouping (e.g., 'birds').
    """
    log(
        f"Received ebird_get_taxonomic_groups request for species grouping: {speciesGrouping}"
    )
    data = await ebird.get_taxonomic_groups(speciesGrouping)
    return {"content": [{"type": "text", "text": format_taxonomic_groups(data)}]}


# ref/region
@mcp.tool(
    name="ebird_get_region_info",
    description="Get information on the name and geographical area covered by a region.",
)
async def ebird_get_region_info(
    regionCode: str,
) -> Dict:
    """1. Get information on the name and geographical area covered by a region.

    :param regionCode: The regional code.
    """
    log(f"Received ebird_get_region_info request for region: {regionCode}")
    data = await ebird.get_region_info(regionCode)
    return {"content": [{"type": "text", "text": format_region_info(data)}]}


@mcp.tool(
    name="ebird_get_sub_region_list",
    description="Get the list of sub-regions for a given country or region.",
)
async def ebird_get_sub_region_list(
    regionType: str,
    parentRegionCode: str,
) -> Dict:
    """2. Get the list of sub-regions for a given country or region.

    :param regionType: The type of region (e.g., 'country', 'state').
    :param parentRegionCode: The regional code of the parent region.
    """
    log(
        f"Received ebird_get_sub_region_list request for region type: {regionType}, parent region: {parentRegionCode}"
    )
    data = await ebird.get_sub_region_list(regionType, parentRegionCode)
    return {"content": [{"type": "text", "text": format_regions(data)}]}


if __name__ == "__main__":
    mcp.run()
