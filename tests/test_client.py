import pytest
import respx

from pyphoton import Photon
from pyphoton.errors import PhotonException


@pytest.mark.asyncio
@respx.mock
async def test_client_simple_request():

    client = Photon()
    expected_json = {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        13.3888599,
                        52.5170365
                    ],
                    "type": "Point"
                },
                "type": "Feature",
                "properties": {
                    "osm_id": 240109189,
                    "osm_type": "N",
                    "country": "Germany",
                    "osm_key": "place",
                    "city": "Berlin",
                    "osm_value": "city",
                    "postcode": "10117",
                    "name": "Berlin",
                    "state": "Berlin"
                }
            }
        ],
        "type": "FeatureCollection"
    }
    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    location = await client.query('berlin', limit=1)

    assert location.longitude == 13.3888599
    assert location.latitude == 52.5170365
    assert location.osm_id == 240109189
    assert location.city == "Berlin"
    assert str(location) == "Berlin\n(52.5170365, 13.3888599)\ncity: Berlin\npostcode: 10117\nstate: Berlin\nosm_id: 240109189\nosm_type: N\nosm_key: place\nosm_value: city"


    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    location = await client.query('berlin', limit=1, bbox=(9.5,51.5,11.5,53.5))
    location = await client.query('berlin', limit=1, bbox="9.5,51.5,11.5,53.5")


@pytest.mark.asyncio
@respx.mock
async def test_client_simple_request_with_extent():

    client = Photon()
    expected_json = {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        12.493087103595503,
                        41.8902614
                    ],
                    "type": "Point"
                },
                "type": "Feature",
                "properties": {
                    "osm_id": 1834818,
                    "osm_type": "R",
                    "extent": [
                        12.4913001,
                        41.8909127,
                        12.4934472,
                        41.8896078
                    ],
                    "country": "Italy",
                    "osm_key": "tourism",
                    "city": "Rome",
                    "street": "Piazza del Colosseo",
                    "osm_value": "attraction",
                    "postcode": "00184",
                    "name": "Colosseum",
                    "state": "Lazio"
                }
            }
        ],
        "type": "FeatureCollection"
    }
    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    location = await client.query('Colosseum', limit=1)

    assert location.longitude == 12.493087103595503
    assert location.latitude == 41.8902614
    assert location.extent_from.longitude == 12.4913001
    assert location.extent_from.latitude == 41.8909127
    assert location.extent_to.longitude == 12.4934472
    assert location.extent_to.latitude == 41.8896078


@pytest.mark.asyncio
@respx.mock
async def test_client_simple_request_with_no_limits():

    client = Photon()
    expected_json = {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        13.3888599,
                        52.5170365
                    ],
                    "type": "Point"
                },
                "type": "Feature",
                "properties": {
                    "osm_id": 240109189,
                    "osm_type": "N",
                    "country": "Germany",
                    "osm_key": "place",
                    "city": "Berlin",
                    "osm_value": "city",
                    "postcode": "10117",
                    "name": "Berlin",
                    "state": "Berlin"
                }
            },
            {
                "geometry": {
                    "coordinates": [
                        12.493087103595503,
                        41.8902614
                    ],
                    "type": "Point"
                },
                "type": "Feature",
                "properties": {
                    "osm_id": 1834818,
                    "osm_type": "R",
                    "extent": [
                        12.4913001,
                        41.8909127,
                        12.4934472,
                        41.8896078
                    ],
                    "country": "Italy",
                    "osm_key": "tourism",
                    "city": "Rome",
                    "street": "Piazza del Colosseo",
                    "osm_value": "attraction",
                    "postcode": "00184",
                    "name": "Berlin Colosseum",
                    "state": "Lazio"
                }
            }
        ],
        "type": "FeatureCollection"
    }
    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    locations = await client.query('berlin')

    assert locations[0].longitude == 13.3888599
    assert locations[0].latitude == 52.5170365
    assert locations[0].name == "Berlin"
    assert str(locations[0]._point) == "(52.5170365, 13.3888599)"

    assert locations[1].longitude == 12.493087103595503
    assert locations[1].latitude == 41.8902614
    assert locations[1].name == 'Berlin Colosseum'

    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    locations = await client.query('berlin', osm_tags=['tourism:attraction', 'place:city'])
    assert locations[0].longitude == 13.3888599
    assert locations[0].latitude == 52.5170365
    assert locations[0].name == "Berlin"

    respx.get('https://photon.komoot.io/api/').respond(json=expected_json)
    location = await client.query('berlin', osm_tags='!place:village')
    assert locations[0].longitude == 13.3888599
    assert locations[0].latitude == 52.5170365
    assert locations[0].name == "Berlin"


@pytest.mark.asyncio
@respx.mock
async def test_reverse():
    expected_json = {
        "features":[
            {
                "geometry":{
                    "coordinates":[
                        9.998645,
                        51.9982968
                    ],
                    "type":"Point"
                },
                "type":"Feature",
                "properties":{
                    "osm_id": 693697564,
                    "osm_type": "N",
                    "country": "Germany",
                    "osm_key": "tourism",
                    "city": "Lamspringe",
                    "street": "Evensener Dorfstraße",
                    "osm_value": "information",
                    "postcode": "31195",
                    "name": "Geographischer Punkt",
                    "state": "Lower Saxony"
                }
            }
        ],
        "type":"FeatureCollection"
    }

    client = Photon()
    respx.get('https://photon.komoot.io/reverse/').respond(json=expected_json)
    location = await client.reverse(latitude=52, longitude=10, limit=1)
    assert location.longitude == 9.998645
    assert location.latitude == 51.9982968
    assert location.osm_id == 693697564

@pytest.mark.asyncio
@respx.mock
async def test_errors():

    client = Photon()
    respx.get('https://photon.komoot.io/api/').respond(json={'message' : "missing search term 'q': /?q=berlin"}, status_code=400)
    with pytest.raises(PhotonException):
        await client.query('berlin', limit=1)

    respx.get('https://photon.komoot.io/api/').respond(status_code=500)
    with pytest.raises(PhotonException):
        await client.query('berlin', limit=1)
