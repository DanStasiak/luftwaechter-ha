# Changelog

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
