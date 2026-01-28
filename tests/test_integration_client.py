import os
import pytest
from pyphoton import Photon

@pytest.mark.asyncio
async def test_client_real_query():

    client = Photon()

    # Perform a real query against the public Photon API
    location = await client.query('berlin', limit=1)

    # Basic sanity checks: coordinates are floats and we got a name or city
    assert isinstance(location.latitude, float)
    assert isinstance(location.longitude, float)

    name = getattr(location, 'name', '') or ''
    city = getattr(location, 'city', '') or ''

    assert (isinstance(name, str) and name) or (isinstance(city, str) and city), "Expected a name or city in the response"

    # Make a weak content assertion to avoid brittle failures
    assert 'berlin' in (name.lower() + city.lower())
