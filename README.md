# Luftwächter for Home Assistant

Room air quality, ventilation advice and window hints, plus a sidebar panel that looks like the
[Luftwächter Windows widget](https://github.com/DanStasiak/airguard-widget). Works for every household user.

## What you get
- A sensor per room (`sensor.luftwaechter_<room>`) with the level (good / fair / poor) and attributes: advice, window hint, readings, devices.
- `sensor.luftwaechter_house` with the whole house at a glance and the outside weather tip.
- A **Luftwächter** entry in the sidebar: room tiles, room details, device buttons (lights, switches, heating, blinds).
- German and English (follows your Home Assistant language). No cloud, no extra requests.

## Install (HACS)
1. HACS → ⋮ → Custom repositories → add `https://github.com/DanStasiak/luftwaechter-ha`, type *Integration*.
2. Download **Luftwächter**, restart Home Assistant.
3. Settings → Devices & services → Add integration → *Luftwächter*. Pick a weather entity (optional).

## How rooms are found
Put your CO₂ and/or fine dust (PM2.5) sensors into an **area**. Temperature, humidity and window sensors in the same area are used too.
Optional: give entities the label `airguard` to choose which sensors and devices are used.

## Limits
| Reading | Good | Fair |
|---|---|---|
| CO₂ | < 1000 ppm | < 1500 ppm |
| Fine dust | < 20 µg/m³ | < 50 µg/m³ |
| Temperature | 17–23 °C | 13–25 °C |
| Humidity | 30–60 % | 25–70 % |

The room level is the worst of the four.

## Development
`pip install pytest-homeassistant-custom-component home-assistant-frontend playwright` then `pytest` and `python tests/panel.spec.py`.

MIT © 2026 Dan Stasiak
