# Changelog

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
