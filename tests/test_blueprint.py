import pathlib

import yaml

BPS = sorted((pathlib.Path(__file__).parent.parent / "blueprints/automation/luftwaechter").glob("*.yaml"))
BP = BPS[0].parent / "level_changed.yaml"


class _L(yaml.SafeLoader):
    pass


_L.add_constructor("!input", lambda loader, node: {"__input__": loader.construct_scalar(node)})


def test_blueprint_is_valid_and_uses_defined_inputs():
    doc = yaml.load(BP.read_text(encoding="utf-8"), Loader=_L)
    bp = doc["blueprint"]
    assert bp["domain"] == "automation" and bp["source_url"].startswith("https://github.com/DanStasiak/luftwaechter-ha/")
    used = set()

    def walk(x):
        if isinstance(x, dict):
            if "__input__" in x:
                used.add(x["__input__"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(doc)
    assert used == set(bp["input"]), (used, set(bp["input"]))
    assert doc["triggers"][0]["event_type"] == "luftwaechter_level_changed"


def test_every_blueprint_is_valid_and_uses_defined_inputs():
    assert len(BPS) >= 2
    for path in BPS:
        doc = yaml.load(path.read_text(encoding="utf-8"), Loader=_L)
        bp = doc["blueprint"]
        assert bp["domain"] == "automation" and bp["source_url"].endswith(path.name), path
        used = set()

        def walk(x):
            if isinstance(x, dict):
                if "__input__" in x:
                    used.add(x["__input__"])
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)

        walk(doc)
        assert used == set(bp["input"]), (path.name, used, set(bp["input"]))
