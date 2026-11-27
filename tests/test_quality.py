"""Repository hygiene tests: translations, services, versions, docs and front-end syntax stay consistent."""
import json
import pathlib
import re
import shutil
import subprocess
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).parent.parent
CC = ROOT / "custom_components" / "luftwaechter"


def _keys(d, prefix=""):
    out = set()
    for k, v in d.items():
        p = f"{prefix}.{k}" if prefix else k
        out.add(p)
        if isinstance(v, dict):
            out |= _keys(v, p)
    return out


def test_strings_json_equals_english_translation():
    assert json.loads((CC / "strings.json").read_text(encoding="utf-8")) == json.loads((CC / "translations" / "en.json").read_text(encoding="utf-8"))


def test_german_translation_has_every_english_key():
    en = json.loads((CC / "translations" / "en.json").read_text(encoding="utf-8"))
    de = json.loads((CC / "translations" / "de.json").read_text(encoding="utf-8"))
    assert _keys(en) - _keys(de) == set(), "missing in de.json"
    assert _keys(de) - _keys(en) == set(), "extra in de.json"


def test_every_option_field_is_labelled_and_described():
    en = json.loads((CC / "translations" / "en.json").read_text(encoding="utf-8"))
    step = en["options"]["step"]["init"]
    src = (CC / "config_flow.py").read_text(encoding="utf-8")
    fields = set(re.findall(r"vol\.(?:Optional|Required)\((CONF_[A-Z0-9_]+)", src))
    const = dict(re.findall(r'^(CONF_[A-Z0-9_]+) = "([a-z0-9_]+)"', (CC / "const.py").read_text(encoding="utf-8"), re.M))
    names = {const[f] for f in fields if f in const}
    assert names - set(step["data"]) == set(), "options without a label"
    assert names - set(step["data_description"]) == set(), "options without a description"


def test_every_service_has_texts_and_an_icon():
    services = yaml.safe_load((CC / "services.yaml").read_text(encoding="utf-8")) or {}
    icons = json.loads((CC / "icons.json").read_text(encoding="utf-8"))["services"]
    for lang in ("en", "de"):
        tr = json.loads((CC / "translations" / f"{lang}.json").read_text(encoding="utf-8"))["services"]
        for name, spec in services.items():
            assert name in tr and tr[name].get("name") and tr[name].get("description"), (lang, name)
            for field in (spec or {}).get("fields", {}):
                assert tr[name]["fields"][field]["name"], (lang, name, field)
    assert set(services) <= set(icons), set(services) - set(icons)


def test_versions_agree_everywhere():
    init = re.search(r'_VERSION = "([^"]+)"', (CC / "__init__.py").read_text(encoding="utf-8")).group(1)
    manifest = json.loads((CC / "manifest.json").read_text(encoding="utf-8"))["version"]
    cff = re.search(r'^version: "([^"]+)"', (ROOT / "CITATION.cff").read_text(encoding="utf-8"), re.M).group(1)
    top = re.search(r"^## ([0-9][^\s]*)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M).group(1)
    assert init == manifest == cff == top


def test_newest_changelog_section_has_german_lines():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    section = re.split(r"^## ", text, flags=re.M)[1]
    assert re.search(r"^- DE: ", section, re.M)


def test_blueprint_reference_page_is_up_to_date():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_blueprint_docs.py"), "--check"], capture_output=True)
    assert r.returncode == 0, "docs/BLUEPRINTS.md is out of date: run python3 tools/gen_blueprint_docs.py"


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
@pytest.mark.parametrize("name", ["luftwaechter-card.js", "luftwaechter-panel.js"])
def test_frontend_files_parse(name):
    r = subprocess.run(["node", "--check", str(CC / "frontend" / name)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_card_documents_every_option_in_the_readme():
    card = (CC / "frontend" / "luftwaechter-card.js").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for opt in re.findall(r"^\s+(\w+):\s+\S.*#", card.split("*/")[0], re.M):
        assert f"`{opt}`" in readme, f"card option {opt} is not in README.md"


@pytest.mark.parametrize("level", ["good", "fair", "poor", "unknown", "neutral"])
def test_mascot_images_exist_in_both_variants(level):
    for name in (f"{level}.png", f"{level}-dark.png"):
        f = CC / "frontend" / "mascot" / name
        assert f.is_file() and f.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"{name} is missing or not a PNG"
        assert f.stat().st_size < 40_000, f"{name} is unexpectedly large"
