import json
import httpx

from .errors import PhotonException
from .models import Location, Point


class Photon:

    def __init__(
            self,
            host='https://photon.komoot.io',
            language='en'
    ):
        self._host = host.strip('/')
        self._language = language

    async def _execute_query(
                self,
                endpoint,
                q=None,
                limit=None,
                lat=None,
                lon=None,
                lang=None,
                location_bias_scale=None,
                osm_tag=None,
                bbox=None
    ):
        # build params as list of tuples so duplicate keys like osm_tag are handled
        params = []
        items = {
            'q': q,
            'limit': limit,
            'lat': lat,
            'lon': lon,
            'lang': lang,
            'location_bias_scale': location_bias_scale
        }
        for k, v in items.items():
            if v is not None:
                params.append((k, v))

        if osm_tag:
            if not isinstance(osm_tag, (list, set, tuple)):
                osm_tag = [osm_tag]
            for osm_tag_el in osm_tag:
                params.append(('osm_tag', osm_tag_el))

        if bbox:
            if isinstance(bbox, (list, set, tuple)):
                bbox = ','.join(map(str, bbox))
            params.append(('bbox', bbox))

        url = f"{self._host}/{endpoint}/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        if response.status_code != 200:
            try:
                json_response = response.json()
            except json.decoder.JSONDecodeError:
                json_response = {'message': 'Error ' + str(response.status_code)}
            raise PhotonException(json_response.get('message', 'Error').capitalize())
        return response.json()

    def _transform_location(self, location):
        new_location = Location()
        location_point = Point(
            location['geometry']['coordinates'][1],
            location['geometry']['coordinates'][0]
        )
        setattr(new_location, '_point', location_point)
        for property_name, property_value in location['properties'].items():
            if property_name == 'extent':
                extent_from = Point(
                    property_value[1],
                    property_value[0]
                )
                extent_to = Point(
                    property_value[3],
                    property_value[2]
                )
                setattr(new_location, 'extent_from', extent_from)
                setattr(new_location, 'extent_to', extent_to)
            else:
                setattr(new_location, property_name, property_value)
        return new_location

    async def query(
                self,
                query,
                limit=None,
                latitude=None,
                longitude=None,
                location_bias_scale=None,
                osm_tags=None,
                bbox=None,
                language=None,
    ):
        if not language:
            language = self._language
        resp = await self._execute_query('api', q=query, limit=limit, lat=latitude, lon=longitude, lang=language, location_bias_scale=location_bias_scale, osm_tag=osm_tags, bbox=bbox)
        return self._transform_locations_from_resp(resp, limit)

    async def reverse(
                self,
                latitude=None,
                longitude=None,
                limit=None,
                language=None,
    ):
        if not language:
            language = self._language
        resp = await self._execute_query('reverse', limit=limit, lat=latitude, lon=longitude, lang=language)
        return self._transform_locations_from_resp(resp, limit)

    def _transform_locations_from_resp(self, resp, limit):
        if limit == 1 and len(resp['features']):
            return self._transform_location(resp['features'][0])
        transformed_locations = []
        for location in resp['features']:
            transformed_locations.append(self._transform_location(location))
        return transformed_locations
