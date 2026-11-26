# What came with which version

Entities are only ever added; none was renamed or removed. After an update, reload the panel (Ctrl+F5) so the browser loads the new panel file.

| Version | New entities / options |
| --- | --- |
| 0.16.0 | `sensor.luftwachter_average_temperature`, `sensor.luftwachter_average_humidity`, option *Mold risk from humidity of* (default 70 %) |
| 0.15.0 | `sensor.luftwachter_average_co2`, `binary_sensor.luftwachter_mold_risk`, icons on every entity |
| 0.14.0 | `sensor.luftwachter_rooms_to_ventilate` |
| 0.13.0 | `binary_sensor.luftwachter_sensor_problem` |
| 0.12.0 | `sensor.luftwachter_good_rooms`, `sensor.luftwachter_worst_room`, `binary_sensor.luftwachter_attention` |
| earlier | one sensor per room, the house sensor, per-room *ventilate* binary sensors |

Blueprints (Settings → Automations → Blueprints → Import): level changed, ventilate reminder, sensor goes quiet, mold warning, daily summary, speak when a room turns poor.

New entities appear after a restart or a reload of the integration. If an entity is missing, check *Settings → Devices & services → Luftwächter → Entities* first; disabled entities are listed there too.
