# Contributing

Thanks for helping. Please open an issue first for bigger changes.

## Setup
```
pip install pytest-homeassistant-custom-component home-assistant-frontend playwright pillow
playwright install chromium
pytest -q                          # engine + Home Assistant setup tests
python tests/panel.spec.py shots   # panel against a mock hass, screenshots in ./shots
python tests/panel.spec.py shots docs   # also refresh the README screenshots
```

## Layout
- `custom_components/luftwaechter/engine.py`: pure Python ratings and advice (no Home Assistant imports, unit tested).
- `coordinator.py` / `sensor.py`: collects areas and entities, exposes the sensors.
- `frontend/luftwaechter-panel.js`: sidebar panel, plain web component, no build step and no external requests.

## Rules
- Keep the limits in `engine.py`, the help texts in the panel and the README table in sync.
- Add German and English text for anything the user sees.
- CI (hassfest, HACS action, tests) must pass.
- Releases: bump `version` in `manifest.json` and add a section to `CHANGELOG.md`; the release workflow tags and publishes on merge to `main`.
