from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.helpers import area_registry as ar, entity_registry as er

DOMAIN = "luftwaechter"


async def test_setup_creates_house_and_room_sensors(hass, enable_custom_integrations):
    areas = ar.async_get(hass)
    ents = er.async_get(hass)
    office = areas.async_create("Office")
    for uid, dc, val in (("co2", "carbon_dioxide", "1300"), ("pm", "pm25", "5")):
        e = ents.async_get_or_create("sensor", "test", uid, original_device_class=dc)
        ents.async_update_entity(e.entity_id, area_id=office.id)
        hass.states.async_set(e.entity_id, val, {"device_class": dc})
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    house = hass.states.get("sensor.luftwaechter_house")
    assert house is not None and house.state == "fair"
    assert house.attributes["rooms"][0]["name"] == "Office"
    room = hass.states.get("sensor.luftwaechter_office")
    assert room is not None and room.attributes["action"] == "open"
