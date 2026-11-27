# Changelog

## 0.21.0
- New: **Lovelace card** `custom:luftwaechter-card` (one room or the whole house). It is added to the dashboards automatically; it follows the Home Assistant language.
- New blueprint **pause heating while a window is open (opt-in)**: snapshot, switch off, restore. Luftwächter itself still never switches anything.
- New blueprint **airing timer, "close the window now"** (speech and/or notification).
- DE: Neu: **Lovelace-Karte** `custom:luftwaechter-card` (ein Raum oder das ganze Haus). Sie wird automatisch zu den Dashboards hinzugefügt und folgt der Home-Assistant-Sprache.
- DE: Neuer Blueprint **Heizung pausieren, solange ein Fenster offen ist (freiwillig)**: Schnappschuss, ausschalten, wiederherstellen. Luftwächter selbst schaltet weiterhin nichts.
- DE: Neuer Blueprint **Lüftungs-Timer „Fenster jetzt schließen“** (Sprache und/oder Meldung).

## 0.20.0
- New: **window reminders.** A window open for the first wait (10 min), while it is colder than your limit outside (10 °C) and inside your active hours (08 to 22), fires the event `luftwaechter_reminder` and repeats every 5 minutes (all adjustable under Configure). New sensors `binary_sensor.luftwachter_window_reminder` and `binary_sensor.luftwachter_<area>_window_reminder`.
- New: **snooze, skip and mute.** Actions `luftwaechter.snooze`, `luftwaechter.skip_until_closed` and `luftwaechter.clear_snooze`; options *Never remind for these windows* and *Mute reminders while on*. Snoozes survive restarts.
- New: **outside temperature sensor** option; it feeds the close-window advice and the reminders (the weather entity stays the fallback).
- New blueprint **window open too long (phone and speakers)** with *Snooze* and *Skip until closed* buttons on the phone notification.
- Four more tests.
- DE: Neu: **Fenster-Erinnerungen.** Ein Fenster, das die erste Wartezeit (10 min) offen ist, während es draußen kälter als Ihre Grenze ist (10 °C) und innerhalb Ihrer aktiven Zeit (8 bis 22 Uhr), löst das Ereignis `luftwaechter_reminder` aus und wiederholt es alle 5 Minuten (alles unter Konfigurieren einstellbar). Neue Sensoren `binary_sensor.luftwachter_window_reminder` und `binary_sensor.luftwachter_<bereich>_window_reminder`.
- DE: Neu: **Schlummern, Überspringen und Stummschalten.** Aktionen `luftwaechter.snooze`, `luftwaechter.skip_until_closed` und `luftwaechter.clear_snooze`; Optionen *Für diese Fenster nie erinnern* und *Erinnerungen stumm, solange an*. Schlummern übersteht Neustarts.
- DE: Neu: Option **Außentemperatur-Sensor**; sie speist den Rat „Fenster schließen“ und die Erinnerungen (die Wetter-Entität bleibt Ersatz).
- DE: Neuer Blueprint **Fenster zu lange offen (Handy und Lautsprecher)** mit den Tasten *Schlummern* und *Bis zum Schließen überspringen* in der Handy-Meldung.

## 0.19.0
- New: **rain sensor.** Luftwächter uses a binary sensor that is on while it rains: the one you pick under Configure → *Rain sensor*, or automatically a binary sensor whose name ends in rain or Regen. With rain, an open window with good air is advised to be closed, and a closed room that needs fresh air is told to wait until the rain stops (unless the air is already stale). Without a rain sensor everything works as before, using the weather entity.
- Three more tests.
- DE: Neu: **Regensensor.** Luftwächter nutzt einen Binärsensor, der bei Regen an ist: den unter Konfigurieren → *Regensensor* gewählten oder automatisch einen Binärsensor, dessen Name auf rain oder Regen endet. Bei Regen wird ein offenes Fenster mit guter Luft zum Schließen geraten, und ein geschlossener Raum, der frische Luft braucht, soll warten, bis der Regen aufhört (außer die Luft ist schon verbraucht). Ohne Regensensor bleibt alles wie bisher über die Wetter-Entität.

## 0.18.0
- New: **smarter "close the window" advice.** A window that is open while the air is good again (CO₂ below your good limit) is now reported as "Please close the window" when it has been open 5 minutes or more and it is below 10 °C outside, or as soon as it rains. The advice shows how long the window has been open.
- New binary sensor `binary_sensor.luftwachter_<room>_close_window` (on while the advice is "close the window") and the house sensor attributes `close` and `close_rooms`. Rooms with a "close" advice now count as needing attention.
- Window contacts are found more reliably: device class window or opening, and door contacts whose name says window or Fenster.
- Nothing is switched automatically. It only changes advice, texts and entities.
- Four more tests.
- DE: Neu: **klügerer Rat „Fenster schließen“.** Ein offenes Fenster bei wieder guter Luft (CO₂ unter Ihrer Grenze) meldet jetzt „Bitte Fenster schließen“, wenn es seit 5 Minuten oder länger offen ist und draußen weniger als 10 °C sind, oder sobald es regnet. Der Rat zeigt, wie lange das Fenster offen ist.
- DE: Neuer Binärsensor `binary_sensor.luftwachter_<Raum>_close_window` (an, solange der Rat „Fenster schließen“ lautet) und die Attribute `close` und `close_rooms` am Haus-Sensor. Räume mit „schließen“ zählen jetzt als „braucht Aufmerksamkeit“.
- DE: Fensterkontakte werden besser erkannt: Geräteklasse Fenster oder Öffnung sowie Türkontakte, deren Name Fenster oder window enthält.
- DE: Es wird nichts automatisch geschaltet. Es ändern sich nur Rat, Texte und Entitäten.

## 0.17.1
- Repaired: the coffee link in the panel help was dark on dark and hard to read; it now uses the theme colour.
- DE: Repariert: Der Kaffee-Link in der Panel-Hilfe war dunkel auf dunkel und schlecht lesbar; er nutzt jetzt die Themenfarbe.

## 0.17.0
- New: a quiet, optional **Buy me a coffee** link in the panel help, a *Sponsor* button on the GitHub page and a short "Support the project" section in the README. Nothing is shown in Home Assistant outside the help dialog.
- DE: Neu: ein dezenter, freiwilliger **Kaffee-Link** in der Panel-Hilfe, ein *Sponsor*-Button auf der GitHub-Seite und ein kurzer Abschnitt „Support the project“ in der README. Außerhalb des Hilfe-Dialogs wird in Home Assistant nichts angezeigt.

## 0.16.0
- New option **Mold risk from humidity of** (50 to 90 %, default 70 %) under Configure. The mold tip, the mold-risk binary sensor and the panel bar all follow it.
- New sensors `sensor.luftwachter_average_temperature` and `sensor.luftwachter_average_humidity`.
- The overview shows an **average line** (CO₂, temperature, humidity) under "rooms good".
- The mold bar no longer says a fixed percentage, so it stays right when you change the limit.
- New keys **A** (browser alerts on / off) and **B** (colour-blind mode). The help lists them.
- New blueprint **speak when a room turns poor** (text to speech on the speakers you pick).
- The README screenshots were regenerated with the current panel.
- New [`docs/UPGRADING.md`](docs/UPGRADING.md): which entities and options came with which version.
- GitHub page: settings text, entities table, keys and FAQ updated (English and German); two more automation examples and dashboard cards for humidity.
- New issue form **Wording or translation**.
- Five more tests (configurable mold limit, averages, new entities, colour-blind key, average line); the blueprint test expects six blueprints.
- DE: Neue Option **Schimmelgefahr ab Luftfeuchte von** (50 bis 90 %, Standard 70 %) unter „Konfigurieren“. Tipp, Binärsensor und Panel-Leiste folgen ihr.
- DE: Neue Sensoren `sensor.luftwachter_average_temperature` und `sensor.luftwachter_average_humidity`.
- DE: Die Übersicht zeigt eine **Durchschnittszeile** (CO₂, Temperatur, Luftfeuchte) unter „Räume gut“.
- DE: Die Schimmel-Leiste nennt keine feste Prozentzahl mehr und bleibt richtig, wenn du die Grenze änderst.
- DE: Neue Tasten **A** (Browser-Hinweise an / aus) und **B** (Farbenblind-Modus). Die Hilfe nennt sie.
- DE: Neuer Blueprint **Sprechen, wenn ein Raum schlecht wird** (Sprachausgabe auf den gewählten Lautsprechern).
- DE: Die Screenshots der Startseite wurden mit dem aktuellen Panel neu erzeugt.
- DE: Neue Seite [`docs/UPGRADING.md`](docs/UPGRADING.md): welche Entitäten und Optionen zu welcher Version kamen.
- DE: GitHub-Seite: Einstellungen, Entitäten, Tasten und FAQ aktualisiert; zwei weitere Beispiele und Dashboard-Karten für Luftfeuchte.
- DE: Neues Ticket-Formular **Formulierung oder Übersetzung**.

## 0.15.0
- New sensor `sensor.luftwachter_average_co2`: average CO₂ of all rooms, ready for a gauge card.
- New binary sensor `binary_sensor.luftwachter_mold_risk`: on while a room's humidity is 70 % or more, with the rooms as attributes.
- The panel shows a **mold-risk bar** (like the quiet-sensor bar) naming the rooms.
- New keys: **E** saves the room history as CSV, **+** and **−** change the text size. The help lists them.
- Every entity now has a fitting icon.
- Two more blueprints: **warn me about mold risk** and **daily air summary** (a message at a time you choose).
- The house sensor carries `co2_avg`, `mold` and `mold_rooms`; the diagnostics also report the integration version, the average CO₂ and mold rooms.
- GitHub page: dashboard ideas ([`docs/DASHBOARD.md`](docs/DASHBOARD.md)), an architecture page with a diagram ([`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)), three new FAQ answers, a Home Assistant version badge, German FAQ.
- Two more automation examples (mold risk, morning summary).
- CONTRIBUTING: a checklist before a pull request; new `.editorconfig`; the issue chooser links to discussions, the FAQ and the security policy.
- Four more tests (average CO₂ and mold in the engine, the new entities and icons, panel keys and mold bar).
- DE: Neuer Sensor `sensor.luftwachter_average_co2`: durchschnittlicher CO₂-Wert aller Räume, passend für eine Tacho-Karte.
- DE: Neuer Binärsensor `binary_sensor.luftwachter_mold_risk`: an, solange in einem Raum die Luftfeuchte 70 % oder mehr beträgt, mit den Räumen als Attribut.
- DE: Das Panel zeigt eine **Schimmel-Leiste** mit den Raumnamen.
- DE: Neue Tasten: **E** speichert den Verlauf als CSV, **+** und **−** ändern die Textgröße. Die Hilfe nennt sie.
- DE: Jede Entität hat jetzt ein passendes Symbol.
- DE: Zwei weitere Blueprints: **Schimmelgefahr melden** und **tägliche Luft-Zusammenfassung** (Nachricht zur gewählten Uhrzeit).
- DE: Haus-Sensor und Diagnose enthalten zusätzliche Werte (Durchschnitts-CO₂, Schimmel-Räume, Version der Integration).
- DE: GitHub-Seite: Dashboard-Ideen, Architektur-Seite mit Schaubild, drei neue FAQ-Antworten, Versions-Abzeichen, deutsche FAQ.
- DE: Zwei weitere Automations-Beispiele (Schimmel, Morgen-Zusammenfassung).
- DE: CONTRIBUTING mit Checkliste, neue `.editorconfig`, der Ticket-Auswahlschirm verweist auf Diskussionen, FAQ und Sicherheitsrichtlinie.

## 0.14.0
- New sensor `sensor.luftwachter_rooms_to_ventilate`: how many rooms advise opening a window right now (the rooms are in its attributes). Good for a dashboard badge or a spoken hint.
- New third **blueprint** "tell me when a sensor goes quiet" for the sensor-problem binary sensor, with a wait time so short gaps are ignored.
- The panel shows a **warning bar** when a room's air sensor has gone quiet, naming the rooms.
- Keys **L** (switch language) and **Home / End** (first / last room); the help lists them.
- The house sensor and the diagnostics now include `silent_rooms` and `ventilate_rooms`, which makes bug reports easier to read.
- New [`docs/AUTOMATION-EXAMPLES.md`](docs/AUTOMATION-EXAMPLES.md) with five copy-and-paste automations.
- GitHub page: entities table, blueprint section, features list and contents bar updated (English and German).
- Three more tests; the blueprint test now expects three blueprints and checks every input is used.
- DE: Neuer Sensor `sensor.luftwachter_rooms_to_ventilate`: wie viele Räume gerade „Fenster öffnen“ raten (die Räume stehen in den Attributen).
- DE: Dritter **Blueprint** „Sag Bescheid, wenn ein Sensor verstummt“ mit Wartezeit.
- DE: Das Panel zeigt eine **Warnleiste**, wenn der Luftsensor eines Raums nichts mehr meldet, mit den Raumnamen.
- DE: Tasten **L** (Sprache wechseln) und **Pos1 / Ende** (erster / letzter Raum); die Hilfe nennt sie.
- DE: Haus-Sensor und Diagnose enthalten jetzt `silent_rooms` und `ventilate_rooms`.
- DE: Neue Sammlung [`docs/AUTOMATION-EXAMPLES.md`](docs/AUTOMATION-EXAMPLES.md) mit fünf Automationen zum Kopieren.
- DE: GitHub-Seite: Entitäten, Blueprints, Funktionsliste und Inhaltsleiste aktualisiert.

## 0.13.0
- **Number keys 1–9** jump straight to a room; **T** cycles the chart range (6 h, 24 h, 7 d). Both are listed in the help.
- The **browser tab title names the room** you are looking at, so several tabs are easy to tell apart.
- New **sensor problem** binary sensor (`binary_sensor.luftwachter_sensor_problem`, diagnostic): on while a room's air sensor has stopped reporting or was ignored as stale. It lists the rooms, so one automation can tell you a battery is empty.
- The house model now carries `silent_rooms` for the same purpose.
- GitHub page: new **Compatibility** and **Uninstall** sections (English and German), the entities table lists the new sensor, and the keyboard lines name the new keys.
- New [`docs/TRANSLATING.md`](docs/TRANSLATING.md): how to add a language to the panel and the advice texts.
- The validation workflow now runs with read-only permissions and cancels superseded runs.
- Three more tests (silent rooms in the engine, the new binary sensor, keys 1–9 / T / tab title in the panel).
- DE: **Zifferntasten 1–9** springen direkt zu einem Raum, **T** schaltet den Zeitraum des Verlaufs um (6 h, 24 h, 7 T). Beides steht in der Hilfe.
- DE: Der **Titel des Browser-Tabs nennt den Raum**, den du ansiehst.
- DE: Neuer Binärsensor **Sensor-Problem** (`binary_sensor.luftwachter_sensor_problem`): an, solange der Luftsensor eines Raums nichts mehr meldet oder als veraltet ignoriert wurde. Er nennt die Räume, so meldet dir eine Automation z. B. eine leere Batterie.
- DE: GitHub-Seite mit neuen Abschnitten **Kompatibilität** und **Deinstallation**; die Entitäten-Tabelle nennt den neuen Sensor.
- DE: Neue Anleitung [`docs/TRANSLATING.md`](docs/TRANSLATING.md) zum Hinzufügen einer Sprache.
- DE: Der Prüf-Workflow läuft mit Nur-Lese-Rechten und bricht überholte Läufe ab.

## 0.12.0
- **Kiosk mode** for wall tablets (key `K`, More menu, or `#kiosk` in the link): biggest text, rooms rotate by themselves, buttons fade out but stay reachable.
- **Browser alerts** (opt-in, More menu): a notification when a room turns poor while the tab is in the background.
- **Language** choice in the More menu (automatic, German, English) for this browser, independent of the profile language.
- **Reset view settings** in the More menu clears pins, sort, size, list view, color-blind mode and the rest if the panel is ever stuck in a state you do not like.
- Settings now keep working when the browser blocks local storage (private window, locked-down kiosk profile): they last until the page is closed instead of silently failing.
- New sensor `sensor.luftwachter_worst_room`: the name of the room with the worst air, for voice assistants and dashboards.
- README: the FAQ folds open and closed, kiosk and alerts are documented, English and German.
- `CITATION.cff`, so GitHub shows "Cite this repository".
- Tests: 34, plus panel checks for language override, kiosk, reset and the new menu entries.
- DE: Kiosk-Modus für Wandtablets (Taste `K`), Browser-Hinweise (optional), Sprachwahl und „Ansicht zurücksetzen“ im Menü, Einstellungen funktionieren auch bei gesperrtem Speicher, neuer Sensor „Schlechtester Raum“, FAQ klappbar, `CITATION.cff`.

## 0.11.0
- New binary sensor per room, `binary_sensor.luftwachter_<room>_ventilate`: on while the advice is "open the window". The simplest trigger for your own automations.
- New blueprint "remind me to ventilate": pick the room's ventilate sensor, set how long the advice must last, choose the action. One-click import badge in the README.
- The overview says how many rooms are fine ("3 of 5 rooms have good air").
- Screen readers announce level changes ("Office: Poor") without moving the focus.
- Tiles show the full advice as a tooltip.
- More menu: "Print / save as PDF" (the print layout hides buttons and menus).
- Blueprint test now checks every blueprint in the folder.
- Tests: 33, plus panel checks for the summary line, tooltip, print entry and announcer.
- README: second blueprint, new entity row and a screen-reader line in the feature list, English and German.
- DE: Neuer Lüften-Sensor pro Raum (`binary_sensor.luftwachter_<raum>_ventilate`), neuer Blueprint „Ans Lüften erinnern“, Übersicht zeigt „3 von 5 Räumen haben gute Luft“, Screenreader-Ansagen bei Wechsel, Tooltips an den Kacheln, Menüpunkt „Drucken / als PDF speichern“.

## 0.10.0
- Help dialog: a proper keyboard shortcut table instead of one long line; the `?` key opens the help too.
- Key `C` copies the house summary (the same text as the menu entry) without opening the menu.
- Touch: swipe left or right in the room view to switch rooms.
- The browser tab title shows the state, e.g. "Luftwächter · 2 of 5 need attention", so you can see it from another tab.
- New sensor `sensor.luftwachter_good_rooms`: the share of rooms with good air in %, with `good` and `total` attributes. Handy for dashboards and automations.
- House sensor attributes `good` and `total`.
- Entity and service icons (`icons.json`).
- Diagnostics download now also lists version, room counts, attention count and the stale limit.
- GitHub: `SUPPORT.md` (where to ask what), README "Quick start" in three steps, updated entity table and contents.
- Tests: 31 (good-rooms sensor, diagnostics) plus panel checks for the shortcut table, `?`, tab title and swipe.
- DE: Tastenkürzel-Tabelle in der Hilfe und `?`-Taste, Taste `C` kopiert die Hausübersicht, Wischen wechselt den Raum, Tab-Titel zeigt den Zustand, neuer Sensor „Gute Räume (%)“, Symbole, mehr Diagnose-Daten, `SUPPORT.md` und Schnellstart im README.

## 0.9.0
- Pin favourite rooms: a ☆ button in the room view (key `P`) keeps a room on top in every sort order, remembered per browser.
- New sort order "Highest CO₂ first"; the sort button now cycles worst first, name, highest CO₂.
- Home Assistant **Repairs** hint when no room has been found for about 5 minutes, with the steps to fix it; it clears itself once a room appears.
- German README (`README.de.md`) with install, settings, entities and troubleshooting.
- README: new "Windows widget" section that explains which of the two to use, and links both ways.
- Tests: 30 (repair issue, sorting, pinning).
- DE: Räume anheften (☆, Taste `P`), neue Sortierung "Höchstes CO₂ zuerst", Reparaturen-Hinweis wenn kein Raum gefunden wird, deutsche README, Abschnitt zum Windows-Widget.

## 0.8.0
- Header decluttered: sorting, filters, list view, rotate, full screen, text size and more now live in a labelled **More** menu (key `M`), with check marks for what is on.
- Tiles show a small sparkline of the last hour, and the tooltip on the level badge tells how long the room has been at that level. The room view shows it too ("Poor for 1 h 35 min"). New room attribute `since` (minutes).
- Color-blind mode (menu): readings get symbols (✓ ! ✕) in addition to colours, on tiles and in the room view.
- "Refresh now" in the menu runs the `luftwaechter.refresh` action from the panel.
- New automation blueprint: react when a room reaches a level (notification, speech, anything), with an optional room filter. Import it from the README.
- Every release now carries `luftwaechter.zip` for manual installs.
- README: blueprint section, manual install steps, download badge, menu screenshot, updated shortcuts and FAQ.
- Tests: 29 (sparkline and time in level, blueprint check) plus new panel checks.
- DE: Menü "Mehr" statt vieler Knöpfe im Kopf, Verlaufslinie auf den Kacheln, "seit wie lange" pro Raum, Farbenblind-Modus, "Jetzt aktualisieren", Automations-Blueprint, ZIP für manuelle Installation bei jeder Version.

## 0.7.0
- Mold risk: rooms at 70 % humidity or more get a warning and a tip, and the room view shows the dew point.
- New entity `binary_sensor.luftwachter_attention`: on while any room is poor or advises opening or waiting. Attributes list the rooms and the worst one.
- The house sensor reports `attention`, `attention_rooms` and `worst_room` for your own automations and cards.
- New option: how many minutes without data before the panel warns (default 10).
- Panel: search box for houses with six or more rooms (press `/`).
- Panel: list view for the overview (press `V`), remembered per browser.
- Panel: optional sound when the ventilation timer ends (bell button), remembered per browser.
- Panel: "Copy link" in the room view for the deep link to that room.
- Accessibility: respects reduced motion and Windows high contrast mode.
- Docs: entity IDs in the README now match the real ones (`sensor.luftwachter_house`).
- Quality: new lint job (ruff and a JavaScript syntax check) in CI, 27 tests.
- DE: Schimmelwarnung ab 70 % Luftfeuchtigkeit mit Taupunkt, neue Entität `binary_sensor.luftwachter_attention`, einstellbare Veraltet-Warnung, Raumsuche, Listenansicht, Signalton für den Lüftungs-Timer, Link kopieren.

## 0.6.0
- Tiles list all four readings, and a new CO₂ ranking card compares the rooms.
- History chart: axis labels, a marker for the latest value, and a CSV download.
- Rotate mode (⟳ or R) steps through the rooms for wall displays; full screen asks the device to keep the screen on.
- Header stays visible while scrolling; the help dialog keeps keyboard focus and returns it when closed.
- Verified in light and dark themes.
- New option: hide areas you do not want in the panel.
- README: animated demo, light theme and phone screenshots, more badges, updated settings and tablet tips.
- DE: Messwerte auf allen Kacheln, CO₂-Vergleich, Achsenbeschriftung und CSV-Export, Durchschalt-Modus, Bereiche ausblenden, Hell/Dunkel geprüft, neue Demo in der README.

## 0.5.0
- Docs: install and update now use the Home Assistant **Marketplace** (it replaced HACS in 2026.11), with the new "Add from link" steps and the risk notice; HACS steps still work on older versions.
- Settings: adjustable CO₂ and fine dust limits (Configure on the integration); panel gauges, help and advice follow them.
- Trend arrows (rising / falling) on tiles and in the room view; `trend` attribute per room.
- Event `luftwaechter_level_changed` whenever a room changes level, for automations.
- Panel: "Only problems" filter and keyboard shortcuts (S, O, F, H, arrows, Esc).
- README: German and timer screenshots, Update, Settings, Events and Roadmap sections. Bug report form asks how you installed and for diagnostics.
- DE: Installation und Update über den Marketplace, einstellbare Grenzwerte für CO₂ und Feinstaub, Trendpfeile, Ereignis `luftwaechter_level_changed`, Filter "Nur Probleme", Tastaturkürzel.

## 0.4.0
- Ventilation timer: start a countdown for the advised time; a header pill follows you between views and a clear alert appears when time is up.
- Overview: house averages (CO₂, fine dust, temperature, humidity), a level label on every tile, a legend for the dots, and "copy house status".
- Full-screen button and deep links (`#room=<key>`), e.g. for wall tablets.
- Built-in guide when no rooms are found yet, and a clear message when the integration is missing.
- Accessibility and layout: main landmark and live status, top-aligned tiles, print-friendly layout.
- New action `luftwaechter.refresh` and downloadable diagnostics for bug reports.
- GitHub page: contents list, how-it-works diagram, FAQ, wall tablet tips, SECURITY, CODE_OF_CONDUCT, CODEOWNERS, Dependabot for workflow updates.
- DE: Lüftungs-Timer, Hausdurchschnitt und Stufen-Label auf den Kacheln, Vollbild und Direktlinks, Einstiegshilfe ohne Räume, Aktion `luftwaechter.refresh`, Diagnosedaten, überarbeitete GitHub-Seite.

## 0.3.1
- Fix: the panel now follows each user's own language (profile setting) instead of the Home Assistant system language. The sensor carries every text in English and German, so one household can use both.
- DE: Korrektur: Das Panel folgt jetzt der Sprache des jeweiligen Benutzers (Profil) statt der Systemsprache von Home Assistant. Alle Texte gibt es auf Englisch und Deutsch.

## 0.3.0
- Overview starts with a "Do now" list: which rooms need attention, click to open the room.
- Every tile shows four indicator dots (CO₂, fine dust, temperature, humidity) coloured by level.
- Text size switch (Aa) for wall tablets, remembered per browser.
- Warning banner when the data is older than 10 minutes; the "updated" time keeps ticking.
- History charts: 6 h, 24 h and 7 day ranges; "Copy status" button in the room view.
- GitHub page: new README with screenshots and "add to HACS" button, issue and pull request templates, CONTRIBUTING, brand logo, and an automatic release workflow.
- DE: Übersicht mit "Jetzt tun", Indikator-Punkte auf den Kacheln, Textgröße, Warnung bei veralteten Daten, Verlauf 6 h / 24 h / 7 Tage, Status kopieren, neue GitHub-Seite.

## 0.2.0
- Room view redesigned: status icon and badge follow the room level (no more green check on a poor room), a "What stands out" list names the problem readings with their limits.
- Readings show a gauge bar with the good / fair / poor zones and a marker.
- New 24 h history chart per reading (CO₂, fine dust, temperature, humidity) with limit zones and hover/touch readout.
- Built-in help: what each reading means, typical causes of bad values and what helps (German and English).
- Devices grouped with state text (on/off, heating, position), open/stop/close for blinds, duplicate names resolved.
- Tiles sort worst-first (or A–Z), the panel remembers your last room, arrow keys / buttons switch rooms, Esc goes back, two-column layout on wide screens, "updated" time in the header.
- DE: Raumansicht neu: Status folgt dem Raumwert, Auffälligkeiten mit Grenzwerten, Skalen, 24-h-Verlauf, Hilfe mit Ursachen, Geräte mit Status und Rollo-Steuerung, Sortierung, Pfeiltasten.

## 0.1.1
- Room tiles now show which reading is the problem (for example "Fine dust: 118 µg/m³") instead of just a red border.
- Panel language follows the integration language, so the header and tiles are no longer mixed German and English.
- Device buttons: no more config/diagnostic entities and no relay switches unless you label them `airguard`.
- Outside temperature no longer shows "-0"; missing humidity is hidden.
- Entity IDs are plain `sensor.luftwachter_<room>` (no area prefix).
- DE: Kacheln zeigen den auffälligen Messwert, Panel-Sprache einheitlich, weniger Geräte-Knöpfe, "-0" behoben, einfachere Entity-IDs.

## 0.1.0
- First version: finds rooms from your Home Assistant areas and rates CO₂, fine dust, temperature and humidity (same limits as the Luftwächter Windows widget).
- One sensor per room plus a house sensor with ventilation and window advice, outside weather hints and rain-soon warning.
- Sidebar panel "Luftwächter" for all household users: room overview, room details, device buttons, German and English.
- DE: Erste Version: Räume aus den Bereichen, gleiche Grenzwerte wie das Windows-Widget, Sensor je Raum, Lüftungsempfehlung, Seitenleisten-Panel für alle Nutzer, Deutsch und Englisch.
