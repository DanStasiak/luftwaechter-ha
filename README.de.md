<p align="center"><img src="https://raw.githubusercontent.com/DanStasiak/luftwaechter-ha/main/custom_components/luftwaechter/brand/icon@2x.png" width="120" alt="Luftwächter"></p>

# Luftwächter für Home Assistant

[![Validate](https://github.com/DanStasiak/luftwaechter-ha/actions/workflows/validate.yml/badge.svg)](https://github.com/DanStasiak/luftwaechter-ha/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/DanStasiak/luftwaechter-ha)](https://github.com/DanStasiak/luftwaechter-ha/releases)
[![Lizenz: MIT](https://img.shields.io/github/license/DanStasiak/luftwaechter-ha)](LICENSE)

Luftqualität pro Raum, Lüftungshinweise und Fensterempfehlungen für Home Assistant, mit einem Seitenleisten-Panel für den ganzen Haushalt. Ergänzung zum [Luftwächter-Widget für Windows](https://github.com/DanStasiak/airguard-widget). Deutsch und Englisch, keine Cloud, keine zusätzlichen Zugänge.  
🇬🇧 [English version](README.md)

<p align="center"><img src="https://raw.githubusercontent.com/DanStasiak/luftwaechter-ha/main/docs/overview_de.png" width="640" alt="Übersicht auf Deutsch"></p>

## Das kann es
- **„Jetzt tun“-Übersicht**: welche Räume Aufmerksamkeit brauchen, der schlechteste zuerst, mit Verlaufslinie der letzten Stunde.
- **Raumansicht**: Status, „Das fällt auf“ mit Grenzwerten, Skalen, Verlauf über 6 Stunden, 24 Stunden oder 7 Tage, Taupunkt und Schimmelwarnung.
- **Lüftungshinweis**: Fenster öffnen, schließen oder offen lassen, wie lange, bei Sturm warten, Regenhinweis aus deiner Wettervorhersage.
- **Lüftungs-Timer** mit Signalton und „Fenster jetzt schließen“.
- **Geräte pro Raum**: Lichter, Heizung, Rollos mit Live-Status.
- **Für gemeinsame Bildschirme**: Textgröße, Vollbild, Durchschalt-Modus, Raumsuche, Listenansicht, angeheftete Lieblingsräume, Farbenblind-Modus.
- **Für deine Automationen**: ein Sensor pro Raum, ein Haus-Sensor, ein „Aufmerksamkeit“-Binärsensor, das Ereignis `luftwaechter_level_changed` und ein Blueprint.
- **Jeder in seiner Sprache**: das Panel folgt der Sprache im Profil des jeweiligen Benutzers.

## Installation (Marketplace)
Home Assistant 2026.11 und neuer hat den **Marketplace** eingebaut (Einstellungen → Marketplace); er hat HACS abgelöst. Auf älteren Versionen: HACS → ⋮ → **Benutzerdefinierte Repositories** (Typ *Integration*).
1. **Einstellungen → Marketplace → Über Link hinzufügen**, dort `https://github.com/DanStasiak/luftwaechter-ha` einfügen. Beim ersten Mal bestätigst du den Risikohinweis; für eigene Projekte braucht es eine GitHub-Verbindung (Home Assistant zeigt einen Code, den du auf GitHub eingibst, ein Passwort wird nicht weitergegeben).
2. **Luftwächter** im Marketplace öffnen, **Herunterladen**, Home Assistant neu starten.
3. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → *Luftwächter*. Optional eine Wetter-Entität wählen.
4. In der Seitenleiste **Luftwächter** öffnen. Sichtbar für alle Benutzer im Haushalt.

**Manuell:** `luftwaechter.zip` von der [aktuellen Version](https://github.com/DanStasiak/luftwaechter-ha/releases/latest) laden, nach `config/custom_components/luftwaechter/` entpacken, Home Assistant neu starten.

Voraussetzung: Home Assistant 2025.10 oder neuer.

## So kommen Räume ins Panel
Weise CO₂-, Feinstaub-, Temperatur- oder Feuchte-Sensoren einem **Bereich** zu (Einstellungen → Bereiche). Der Raum erscheint von selbst, sobald ein Sensor Werte meldet. Ein Fenstersensor mit der Geräteklasse „window“ liefert zusätzlich „Fenster öffnen / schließen“. Findet Luftwächter länger als etwa 5 Minuten keinen Raum, zeigt Home Assistant unter **Einstellungen → Reparaturen** einen Hinweis.

## Einstellungen
**Einstellungen → Geräte & Dienste → Luftwächter → Konfigurieren**: Wetter-Entität, Bereiche ausblenden, Grenzwerte für CO₂ und Feinstaub (Standard 1000 / 1500 ppm und 20 / 50 µg/m³) und nach wie vielen Minuten ohne Daten das Panel warnt (Standard 10).

## Entitäten
| Entität | Zustand | Attribute |
|---|---|---|
| `sensor.luftwachter_<raum>` | good / fair / poor | action, headline, detail, window, trend, since, mold, dew, values, devices |
| `sensor.luftwachter_house` | schlechtester Wert | rooms, outside, limits, attention, attention_rooms, worst_room |
| `binary_sensor.luftwachter_attention` | an, solange ein Raum schlecht ist oder Lüften/Warten rät | count, rooms, worst_room |

Die Entity-IDs hängen von deiner Installation ab. Ereignis und Blueprint sind in der [englischen Beschreibung](README.md#events-for-automations) erklärt; der Blueprint lässt sich mit einem Klick importieren:

[![Blueprint importieren](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDanStasiak%2Fluftwaechter-ha%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fluftwaechter%2Flevel_changed.yaml)

## Tastatur
← → Raum wechseln · Esc zurück · `/` suchen · `S` sortieren (schlechtester, Name, CO₂) · `P` Raum anheften · `O` nur Probleme · `V` Listenansicht · `M` Menü · `R` durchschalten · `F` Vollbild · `H` Hilfe

## Fehlersuche
- **Panel zeigt noch alte Texte nach dem Update**: Browser-Seite hart neu laden (Strg + F5).
- **Kein Raum sichtbar**: Sensoren einem Bereich zuweisen, siehe oben; Reparaturen prüfen.
- **Fehler melden**: [Issue öffnen](https://github.com/DanStasiak/luftwaechter-ha/issues/new/choose); die Diagnosedaten der Integration helfen dabei.

## Datenschutz
Alles läuft in deinem Home Assistant. Keine Konten, keine Cloud-Dienste, keine Telemetrie.

MIT © 2026 Dan Stasiak
