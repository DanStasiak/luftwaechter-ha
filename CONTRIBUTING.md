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

## Before you open a pull request
1. `ruff check custom_components` and `node --check custom_components/luftwaechter/frontend/luftwaechter-panel.js` are clean.
2. `pytest -q` and `python tests/panel.spec.py shots` pass.
3. New user-visible text exists in German and English; new keyboard keys are in the help table and both READMEs.
4. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the pieces fit and [docs/TRANSLATING.md](docs/TRANSLATING.md) to add a language.

## Layout
- `custom_components/luftwaechter/engine.py`: pure Python ratings and advice (no Home Assistant imports, unit tested).
- `coordinator.py` / `sensor.py`: collects areas and entities, exposes the sensors.
- `frontend/luftwaechter-panel.js`: sidebar panel, plain web component, no build step and no external requests.

## Rules
- Keep the limits in `engine.py`, the help texts in the panel and the README table in sync.
- Add German and English text for anything the user sees.
- CI (hassfest, Marketplace/HACS repository check, tests) must pass.
- Releases: bump `version` in `manifest.json` and add a section to `CHANGELOG.md`; the release workflow tags and publishes on merge to `main`.
