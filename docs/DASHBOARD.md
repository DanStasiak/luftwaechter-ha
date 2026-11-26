# Dashboard ideas

Entity IDs depend on your rooms; replace `office` with your room name.

## Tile card for the house
```yaml
type: tile
entity: sensor.luftwachter_house
name: Air
vertical: true
```

## Gauge for the average CO₂
```yaml
type: gauge
entity: sensor.luftwachter_average_co2
min: 400
max: 2000
severity:
  green: 400
  yellow: 1000
  red: 1500
```

## Badges for the things that need you
```yaml
badges:
  - type: entity
    entity: sensor.luftwachter_rooms_to_ventilate
  - type: entity
    entity: binary_sensor.luftwachter_mold_risk
  - type: entity
    entity: binary_sensor.luftwachter_sensor_problem
```

## One room, history
```yaml
type: history-graph
hours_to_show: 24
entities:
  - sensor.luftwachter_office
```

## Open the full panel from a button
```yaml
type: button
name: Luftwächter
icon: mdi:air-filter
tap_action:
  action: navigate
  navigation_path: /luftwaechter
```
