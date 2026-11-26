# Automation examples

Copy, paste, adjust. Replace the notify and speaker entities with your own. Prefer clicks? The [blueprints](../README.md#blueprint) cover the first three.

## 1. A room became poor
```yaml
triggers:
  - trigger: event
    event_type: luftwaechter_level_changed
    event_data:
      level: poor
actions:
  - action: notify.mobile_app_phone
    data:
      message: "{{ trigger.event.data.room }}: {{ trigger.event.data.headline }}"
```

## 2. Open the window, but only after 5 minutes
```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.luftwachter_office_ventilate
    to: "on"
    for: "00:05:00"
actions:
  - action: notify.mobile_app_phone
    data:
      message: "{{ state_attr(trigger.entity_id, 'headline') }}"
```

## 3. A sensor went quiet
```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.luftwachter_sensor_problem
    to: "on"
    for: "00:30:00"
actions:
  - action: notify.mobile_app_phone
    data:
      message: "Air sensor silent in: {{ state_attr('binary_sensor.luftwachter_sensor_problem', 'rooms') | join(', ') }}"
```

## 4. Say it out loud when several rooms need air
```yaml
triggers:
  - trigger: numeric_state
    entity_id: sensor.luftwachter_rooms_to_ventilate
    above: 1
actions:
  - action: tts.speak
    target:
      entity_id: tts.piper
    data:
      media_player_entity_id: media_player.kitchen
      message: "{{ states('sensor.luftwachter_rooms_to_ventilate') }} rooms need fresh air."
```

## 5. Dashboard badge
Use `sensor.luftwachter_rooms_to_ventilate` (a number) or `binary_sensor.luftwachter_attention` (on / off) in any badge or tile card.
