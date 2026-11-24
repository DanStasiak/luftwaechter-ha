# Changelog

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
