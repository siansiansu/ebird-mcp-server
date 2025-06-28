import httpx


class EBirdClient:
    """
    eBird Client
    A simple API client for eBird API v2.
    Ref: https://documenter.getpostman.com/view/664302/S1ENwy59
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ebird.org/v2"

    async def make_request(self, endpoint, params=None, expect_json=True):
        """
        Make an async request to the eBird API.
        It automatically handles boolean to string conversion for API parameters.
        """
        if params is None:
            params = {}

        processed_params = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                processed_params[key] = "true" if value else "false"
            else:
                processed_params[key] = value

        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-eBirdApiToken": self.api_key,
            "Accept": "application/json" if expect_json else "text/plain",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.get(
                    url, headers=headers, params=processed_params
                )
                response.raise_for_status()

                if expect_json:
                    return response.json()
                else:
                    return response.text

            except httpx.RequestError as e:
                print(f"Request error while accessing {url}: {e}")
                raise
            except httpx.HTTPStatusError as e:
                print(f"HTTP error while accessing {url}: {e}")
                raise

    # --- data/obs ---
    async def get_recent_observations(self, region_code, options=None):
        """
        1. Recent observations in a region.
        """
        if options is None:
            options = {}

        detail = options.get("detail", "simple")
        params = {
            "back": options.get("back", 14),
            "maxResults": options.get("maxResults", 100),
            "includeProvisional": options.get("includeProvisional", True),
            "hotspot": options.get("hotspot", False),
        }

        if detail == "full":
            endpoint = f"/data/obs/{region_code}/recent/detailed"
        else:
            endpoint = f"/data/obs/{region_code}/recent"

        return await self.make_request(endpoint, params)

    async def get_notable_observations(self, region_code, options=None):
        """
        2. Recent notable observations in a region.
        """
        if options is None:
            options = {}

        detail = options.get("detail", "simple")
        params = {
            "back": options.get("back", 14),
            "maxResults": options.get("maxResults", 100),
        }

        if detail == "full":
            endpoint = f"/data/obs/{region_code}/recent/notable/detailed"
        else:
            endpoint = f"/data/obs/{region_code}/recent/notable"

        return await self.make_request(endpoint, params)

    async def get_recent_observations_for_species(
        self, region_code, species_code, options=None
    ):
        """
        3. Recent observations of a species in a region.
        """
        if options is None:
            options = {}

        params = {
            "back": options.get("back", 14),
            "maxResults": options.get("maxResults", 100),
            "includeProvisional": options.get("includeProvisional", True),
            "hotspot": options.get("hotspot", False),
        }

        endpoint = f"/data/obs/{region_code}/recent/{species_code}"

        return await self.make_request(endpoint, params)

    async def get_nearby_observations(self, lat, lng, options=None):
        """
        4. Recent nearby observations.
        """
        if options is None:
            options = {}

        params = {
            "lat": lat,
            "lng": lng,
            "back": options.get("back", 14),
            "dist": options.get("dist", 25),
            "maxResults": options.get("maxResults", 100),
            "includeProvisional": options.get("includeProvisional", True),
            "hotspot": options.get("hotspot", False),
        }

        endpoint = "/data/obs/geo/recent"

        return await self.make_request(endpoint, params)

    async def get_nearby_observations_for_species(
        self, lat, lng, species_code, options=None
    ):
        """
        5. Recent nearby observations of a species.
        """
        if options is None:
            options = {}

        params = {
            "lat": lat,
            "lng": lng,
            "back": options.get("back", 14),
            "dist": options.get("dist", 25),
            "maxResults": options.get("maxResults", 100),
            "includeProvisional": options.get("includeProvisional", True),
        }

        endpoint = f"/data/obs/geo/recent/{species_code}"

        return await self.make_request(endpoint, params)

    async def get_nearest_observations_for_species(
        self, lat, lng, species_code, options=None
    ):
        """
        6. Nearest observations of a species.
        """
        if options is None:
            options = {}

        params = {
            "lat": lat,
            "lng": lng,
            "back": options.get("back", 14),
            "dist": options.get("dist", 25),
            "maxResults": options.get("maxResults", 100),
            "includeProvisional": options.get("includeProvisional", True),
        }

        endpoint = f"/data/nearest/geo/recent/{species_code}"

        return await self.make_request(endpoint, params)

    async def get_nearby_notable_observations(self, lat, lng, options=None):
        """
        7. Recent nearby notable observations.
        """
        if options is None:
            options = {}

        params = {
            "lat": lat,
            "lng": lng,
            "back": options.get("back", 14),
            "dist": options.get("dist", 25),
            "maxResults": options.get("maxResults", 100),
        }

        endpoint = "/data/obs/geo/recent/notable"

        return await self.make_request(endpoint, params)

    async def get_historic_observations(
        self, region_code, year, month, day, options=None
    ):
        """
        8. Historic observations on a date.
        """
        if options is None:
            options = {}

        params = {
            "back": options.get("back", 14),
            "maxResults": options.get("maxResults", 100),
        }

        endpoint = f"/data/obs/{region_code}/historic/{year}/{month}/{day}"

        return await self.make_request(endpoint, params)

    # --- product ---
    async def get_top100(self, region_code, year, month, day):
        """
        1. Top 100.
        """
        endpoint = f"/product/top100/{region_code}/{year}/{month}/{day}"
        return await self.make_request(endpoint)

    async def get_recent_checklists_feed(self, region_code):
        """
        2. Recent checklists feed
        """
        endpoint = f"/product/lists/{region_code}"
        return await self.make_request(endpoint)

    async def get_checklist_feed_on_date(self, region_code, year, month, day):
        """
        3. Checklist feed on a date.
        """
        endpoint = f"/product/lists/{region_code}/{year}/{month}/{day}"
        return await self.make_request(endpoint)

    async def get_regional_statistics_on_date(self, region_code, year, month, day):
        """
        4. Regional statistics on a date.
        """
        endpoint = f"/product/stats/{region_code}/{year}/{month}/{day}"
        return await self.make_request(endpoint)

    async def get_species_list_for_region(self, region_code):
        """
        5. Species List for a Region.
        """
        endpoint = f"/product/spplist/{region_code}"
        return await self.make_request(endpoint)

    async def get_checklist(self, checklist_id):
        """
        6. View Checklist
        """
        endpoint = f"/product/checklist/view/{checklist_id}"
        return await self.make_request(endpoint)

    # --- ref/geo ---
    async def get_adjacent_regions(self, region_code):
        """
        1. Adjacent Regions.
        """
        endpoint = f"/ref/adjacent/{region_code}"
        return await self.make_request(endpoint)

    # --- ref/hotspot ---
    async def get_hotspots(self, region_code, options=None):
        """
        1. Hotspots in a region.
        """
        if options is None:
            options = {}

        params = {
            "back": options.get("back", 14),
            "includeProvisional": options.get("includeProvisional", True),
        }

        endpoint = f"/ref/hotspot/{region_code}"

        return await self.make_request(endpoint, params)

    async def get_nearby_hotspots(self, lat, lng, options=None):
        """
        2. Nearby hotspots.
        """
        if options is None:
            options = {}

        params = {
            "lat": lat,
            "lng": lng,
            "dist": options.get("dist", 25),
            "back": options.get("back", 14),
            "includeProvisional": options.get("includeProvisional", True),
            "fmt": options.get("fmt", "json"),
        }

        endpoint = "/ref/hotspot/geo"

        try:
            return await self.make_request(endpoint, params)
        except Exception:
            print("Falling back to text format for hotspots.")
            params.pop("fmt", None)
            text_response = await self.make_request(endpoint, params, expect_json=False)
            if text_response:
                location_ids = [
                    id.strip() for id in text_response.split(",") if id.strip()
                ]
                return [
                    {
                        "locId": loc_id,
                        "locName": f"Hotspot {loc_id}",
                        "lat": lat,
                        "lng": lng,
                        "numSpecies": None,
                        "isHotspot": True,
                    }
                    for loc_id in location_ids
                ]
            return []

    async def get_hotspot_info(self, loc_id):
        """
        3. Hotspot Info.
        """
        endpoint = f"/ref/hotspot/info/{loc_id}"
        return await self.make_request(endpoint)

    # --- ref/taxonomy ---
    async def get_taxonomy(self, options=None):
        """
        1. eBird Taxonomy.
        """
        if options is None:
            options = {}

        params = {
            "locale": options.get("locale", "en"),
            "cat": options.get("cat", "species"),
            "fmt": options.get("fmt", "json"),
        }

        endpoint = "/ref/taxonomy/ebird"

        return await self.make_request(endpoint, params)

    async def get_taxonomy_forms(self, species_code):
        """
        2. Taxonomic Forms.
        """
        endpoint = f"/ref/taxonomy/forms/{species_code}"
        return await self.make_request(endpoint)

    async def get_taxa_locale_codes(self):
        """
        3. Taxa Locale Codes.
        """
        endpoint = "/ref/taxa-locales/ebird"
        return await self.make_request(endpoint)

    async def get_taxonomy_versions(self):
        """
        4. Taxonomy Versions.
        """
        endpoint = "/ref/taxonomy/versions"
        return await self.make_request(endpoint)

    async def get_taxonomic_groups(self, species_grouping):
        """
        5. Taxonomic Groups.
        """
        endpoint = f"/ref/sppgroup/{species_grouping}"
        return await self.make_request(endpoint)

    # --- ref/region ---
    async def get_region_info(self, region_code):
        """
        1. Region Info.
        """
        endpoint = f"/ref/region/info/{region_code}"
        return await self.make_request(endpoint)

    async def get_sub_region_list(self, region_type, parent_region_code):
        """
        2. Sub Region List.
        """
        endpoint = f"/ref/region/list/{region_type}/{parent_region_code}"
        return await self.make_request(endpoint)
