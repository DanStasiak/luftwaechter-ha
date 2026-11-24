import pathlib

import custom_components

pytest_plugins = "pytest_homeassistant_custom_component"

# the test plugin ships its own `custom_components` package; make ours visible too
_ours = str(pathlib.Path(__file__).parent.parent / "custom_components")
if _ours not in list(custom_components.__path__):
    custom_components.__path__.append(_ours)
