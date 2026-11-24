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
    house = hass.states.get("sensor.luftwachter_house")
    assert house is not None and house.state == "fair"
    assert house.attributes["rooms"][0]["name"] == "Office"
    room = hass.states.get("sensor.luftwachter_office")
    assert room is not None and room.attributes["action"] == "open"


async def test_refresh_service_and_diagnostics(hass, enable_custom_integrations):
    from custom_components.luftwaechter.diagnostics import async_get_config_entry_diagnostics

    areas = ar.async_get(hass)
    ents = er.async_get(hass)
    office = areas.async_create("Office")
    e = ents.async_get_or_create("sensor", "test", "co2", original_device_class="carbon_dioxide")
    ents.async_update_entity(e.entity_id, area_id=office.id)
    hass.states.async_set(e.entity_id, "700", {"device_class": "carbon_dioxide"})
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.services.has_service(DOMAIN, "refresh")
    hass.states.async_set(e.entity_id, "1600", {"device_class": "carbon_dioxide"})
    await hass.services.async_call(DOMAIN, "refresh", blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.luftwachter_house").state == "poor"
    diag = await async_get_config_entry_diagnostics(hass, entry)
    assert diag["rooms"][0]["values"]["co2"] == 1600 and diag["level"] == "poor"


async def _setup(hass, co2="700", options=None):
    areas = ar.async_get(hass)
    ents = er.async_get(hass)
    office = areas.async_create("Office")
    e = ents.async_get_or_create("sensor", "test", "co2", original_device_class="carbon_dioxide")
    ents.async_update_entity(e.entity_id, area_id=office.id)
    hass.states.async_set(e.entity_id, co2, {"device_class": "carbon_dioxide"})
    entry = MockConfigEntry(domain=DOMAIN, data={}, options=options or {})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry, e.entity_id


async def test_level_change_event_and_trend(hass, enable_custom_integrations):
    import time

    from pytest_homeassistant_custom_component.common import async_capture_events

    entry, eid = await _setup(hass, "700")
    coord = hass.data[DOMAIN][entry.entry_id]
    events = async_capture_events(hass, "luftwaechter_level_changed")
    key = coord.data["rooms"][0]["key"]
    coord._samples[key].append((time.time() - 900, "co2", 600))
    hass.states.async_set(eid, "1600", {"device_class": "carbon_dioxide"})
    await hass.services.async_call(DOMAIN, "refresh", blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.luftwachter_office").attributes["trend"] == "up"
    assert len(events) == 1 and events[0].data["from"] == "good" and events[0].data["to"] == "poor"
    assert events[0].data["room"] == "Office"


async def test_options_flow_validates_and_applies_limits(hass, enable_custom_integrations):
    entry, _ = await _setup(hass, "1300")
    assert hass.states.get("sensor.luftwachter_house").state == "fair"
    flow = await hass.config_entries.options.async_init(entry.entry_id)
    bad = await hass.config_entries.options.async_configure(
        flow["flow_id"], {"co2_good": 2000, "co2_fair": 1000, "pm_good": 20, "pm_fair": 50}
    )
    assert bad["errors"] == {"base": "limits_order"}
    ok = await hass.config_entries.options.async_configure(
        flow["flow_id"], {"co2_good": 1500, "co2_fair": 2000, "pm_good": 20, "pm_fair": 50}
    )
    assert ok["type"] == "create_entry"
    await hass.async_block_till_done()
    assert hass.states.get("sensor.luftwachter_house").state == "good"


async def test_excluded_areas_are_hidden(hass, enable_custom_integrations):
    entry, _ = await _setup(hass, "700")
    assert hass.states.get("sensor.luftwachter_office") is not None
    area_id = hass.data[DOMAIN][entry.entry_id].data["rooms"][0]["key"]
    flow = await hass.config_entries.options.async_init(entry.entry_id)
    res = await hass.config_entries.options.async_configure(
        flow["flow_id"],
        {"co2_good": 1000, "co2_fair": 1500, "pm_good": 20, "pm_fair": 50, "excluded_areas": [area_id]},
    )
    assert res["type"] == "create_entry"
    await hass.async_block_till_done()
    assert hass.data[DOMAIN][entry.entry_id].data["rooms"] == []


async def test_attention_binary_sensor(hass, enable_custom_integrations):
    entry, eid = await _setup(hass, co2="1600")
    b = hass.states.get("binary_sensor.luftwachter_attention")
    assert b is not None and b.state == "on"
    assert b.attributes["rooms"] == ["Office"] and b.attributes["count"] == 1
    hass.states.async_set(eid, "600", {"device_class": "carbon_dioxide"})
    await hass.services.async_call(DOMAIN, "refresh", blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.luftwachter_attention").state == "off"
    house = hass.states.get("sensor.luftwachter_house")
    assert house.attributes["attention"] == 0 and house.attributes["stale_min"] == 10


async def test_stale_minutes_option(hass, enable_custom_integrations):
    await _setup(hass, options={"stale_minutes": 30})
    assert hass.states.get("sensor.luftwachter_house").attributes["stale_min"] == 30
