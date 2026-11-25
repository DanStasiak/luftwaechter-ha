# Adding a language

Luftwächter has two sets of texts. Both are plain data, no build step.

1. **Panel texts**: in `custom_components/luftwaechter/frontend/luftwaechter-panel.js`, copy the `en` block of the `UI` object, rename it to your language code (for example `fr`) and translate the values. Keep placeholders such as `{r}` and `{l}` unchanged.
2. **Advice texts**: in `custom_components/luftwaechter/engine.py`, copy the `en` block of `TEXTS` and translate it the same way. Keep placeholders such as `{n}` and `{m}`.
3. Add the language code to the list used by `_cycleLang` in the panel, so the More menu can select it.
4. Run the checks: `pytest -q` (`test_texts_in_every_language` fails when a key is missing) and `python tests/panel.spec.py shots`.
5. Add a line to `CHANGELOG.md` and open a pull request.

Home Assistant itself needs no change: the panel follows each user's profile language, or the choice made in the More menu.
