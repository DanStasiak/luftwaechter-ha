"""Builds docs/BLUEPRINTS.md from the blueprint files, so the list of inputs can never go out of date.

Run:  python3 tools/gen_blueprint_docs.py        (writes the file)
      python3 tools/gen_blueprint_docs.py --check (exit 1 when the file is out of date; used by the tests)
"""
from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
BPS = ROOT / "blueprints" / "automation" / "luftwaechter"
OUT = ROOT / "docs" / "BLUEPRINTS.md"
REPO = "https://github.com/DanStasiak/luftwaechter-ha"


class _L(yaml.SafeLoader):
    pass


_L.add_constructor("!input", lambda loader, node: {"__input__": loader.construct_scalar(node)})


def _one_line(text: object) -> str:
    return " ".join(str(text or "").split()).replace("|", "\\|")


def render() -> str:
    lines = [
        "# Blueprints",
        "",
        "Luftwächter ships ready-made automations as Home Assistant blueprints. This page is generated from the files in",
        "`blueprints/automation/luftwaechter/` (do not edit it by hand: run `python3 tools/gen_blueprint_docs.py`).",
        "",
        "Marketplace/HACS does not copy blueprints for you. Import one with the button in its section, or in Home Assistant:",
        "**Settings → Automations & scenes → Blueprints → Import blueprint** and paste the link.",
        "",
    ]
    for path in sorted(BPS.glob("*.yaml")):
        doc = yaml.load(path.read_text(encoding="utf-8"), Loader=_L)
        bp = doc["blueprint"]
        raw = f"{REPO}/blob/main/blueprints/automation/luftwaechter/{path.name}"
        lines += [
            f"## {bp['name']}",
            "",
            _one_line(bp.get("description")),
            "",
            f"[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url={raw})",
            "",
            "| Input | Default | What it does |",
            "| --- | --- | --- |",
        ]
        for key, spec in bp.get("input", {}).items():
            default = spec.get("default", "")
            default = "(empty)" if default in ("", [], None) else f"`{default}`"
            lines.append(f"| {_one_line(spec.get('name', key))} (`{key}`) | {_one_line(default)} | {_one_line(spec.get('description', ''))} |")
        lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = render()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding="utf-8") == text else 1)
    OUT.write_text(text, encoding="utf-8")
    print("wrote", OUT)
