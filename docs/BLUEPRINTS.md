# Blueprints

Luftwächter ships ready-made automations as Home Assistant blueprints. This page is generated from the files in
`blueprints/automation/luftwaechter/` (do not edit it by hand: run `python3 tools/gen_blueprint_docs.py`).

Marketplace/HACS does not copy blueprints for you. Import one with the button in its section, or in Home Assistant:
**Settings → Automations & scenes → Blueprints → Import blueprint** and paste the link.

## Luftwächter - airing timer, "close the window now" (spoken or push)

When a window is opened, waits until the window is closed again, until Luftwächter's "close window" sensor of the room turns on, or until your time is up (short airing, for example 5 minutes), whichever comes first. If the window is still open then, it tells you to close it by speech and/or a notification.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/airing_timer.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Window contact (`window`) | (empty) |  |
| Luftwächter "close window" sensor of the room (optional) (`close_sensor`) | (empty) |  |
| Airing time (minutes) (`minutes`) | `5` |  |
| Text to speech engine (optional) (`tts_entity`) | (empty) |  |
| Speakers (`speakers`) | (empty) |  |
| Voice on/off switch (optional) (`speak_switch`) | (empty) | Pick an input_boolean or switch. The voice is only spoken while it is on; the phone push is not affected. Leave empty for always on. |
| Notify service (optional) (`notify_service`) | (empty) | For example notify.mobile_app_my_phone. |
| Text (`text`) | `Please close the window now.` |  |

## Luftwächter - daily air summary

Runs your actions once a day at the time you choose, for example "send the air summary at 8:00". In your actions you can use the variables `good`, `total`, `worst_room` and `to_ventilate`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/daily_summary.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| House sensor (`house_sensor`) | (empty) | The sensor "Luftwächter House". |
| Time of day (`run_at`) | `08:00:00` |  |
| Actions (`actions`) | (empty) | What to do, for example send a notification. Use {{ good }}, {{ total }}, {{ worst_room }} and {{ to_ventilate }} in texts. |

## Luftwächter - pause heating while a window is open (opt-in)

Optional and entirely your choice: when a window has been open for a while, the thermostats you pick are switched off, and when all picked windows have been closed for a short time, their previous state (mode, target temperature) is restored from a snapshot. Luftwächter itself never switches heating; this blueprint does only what you set up here. Tip: with the *window open too long* reminders you may not need it.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/heating_pause.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Window contacts (`windows`) | (empty) | The windows that should pause the heating (all of them must be closed to restore). |
| Thermostats (`thermostats`) | (empty) | The heating devices to switch off while a window is open. |
| Window open for (seconds) (`open_seconds`) | `120` |  |
| All windows closed for (seconds) (`closed_seconds`) | `30` |  |

## Luftwächter - react when a room changes level

Runs your actions when a room reaches a chosen air quality level, for example "send a notification when a room becomes poor". Uses the event that the Luftwächter integration fires on every level change. In your actions you can use the variables `room`, `headline`, `level` and `previous`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/level_changed.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Level that triggers the actions (`to_level`) | `poor` | The room must change to this level. |
| Room name (optional) (`room_filter`) | (empty) | Leave empty for all rooms, or enter one room name exactly as shown in the panel. |
| Actions (`actions`) | (empty) | What to do, for example send a notification or speak a message. Use {{ room }} and {{ headline }} in texts. |

## Luftwächter - warn me about mold risk

Runs your actions when a room's humidity stays high (70 % or more) for the time you choose. In your actions you can use the variables `rooms` (a list of room names) and `count`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/mold_warning.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Mold risk (`mold_sensor`) | (empty) | The binary sensor "Luftwächter Mold risk". |
| Wait before warning (minutes) (`wait_minutes`) | `60` | The humidity must stay high this long, so a hot shower is ignored. |
| Actions (`actions`) | (empty) | What to do, for example send a notification. Use {{ rooms }} and {{ count }} in texts. |

## Luftwächter - tell me when a sensor goes quiet

Runs your actions when a room's air sensor has stopped reporting (for example an empty battery) for the time you choose. In your actions you can use the variables `rooms` (a list of room names) and `count`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/sensor_problem.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Sensor problem (`problem_sensor`) | (empty) | The binary sensor "Luftwächter Sensor problem". |
| Wait before telling me (minutes) (`wait_minutes`) | `30` | The problem must last this long, so a short Wi-Fi gap is ignored. |
| Actions (`actions`) | (empty) | What to do, for example send a notification. Use {{ rooms }} and {{ count }} in texts. |

## Luftwächter - speak when a room turns poor

Says a short hint out loud (text to speech) when a room's air becomes poor, for example with Piper. In your text you can use `{{ room }}` and `{{ headline }}`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/speak_when_poor.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Text to speech (`tts_engine`) | (empty) |  |
| Speakers (`speakers`) | (empty) |  |
| Text (`message`) | `{{ room }}: {{ headline }}` |  |

## Luftwächter - remind me to ventilate

Runs your actions when Luftwächter advises opening a window in a room and the advice has lasted for the time you choose, for example "send a notification after 5 minutes". Pick the room's "ventilate" sensor. In your actions you can use the variables `room` and `headline`.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/ventilate_reminder.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Room (ventilate sensor) (`ventilate_sensor`) | (empty) | The binary sensor "Luftwächter <room> ventilate" of the room to watch. |
| Wait before reminding (minutes) (`wait_minutes`) | `5` | The advice must last this long before the actions run, so short peaks are ignored. |
| Actions (`actions`) | (empty) | What to do, for example send a notification. Use {{ room }} and {{ headline }} in texts. |

## Luftwächter - window open too long (phone and speakers)

Sends a push notification to your phone and optionally speaks on speakers when Luftwächter reminds you that a window has been open too long (first wait, repeat, cold outside and active hours are set in the integration's options). The phone notification has two buttons: "Snooze" and "Skip until closed". Replaces a hand-built "window open too long" automation. Note: the standard Home Assistant companion app push is relayed through the Google or Apple push service.

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/DanStasiak/luftwaechter-ha/blob/main/blueprints/automation/luftwaechter/window_reminder.yaml)

| Input | Default | What it does |
| --- | --- | --- |
| Phone notify service (`notify_service`) | (empty) | The notify action of your phone, for example notify.mobile_app_my_phone. Leave empty to skip the push. |
| Snooze length (minutes) (`snooze_minutes`) | `15` |  |
| Text to speech engine (`tts_entity`) | (empty) | Optional. Pick a TTS engine and at least one speaker to also speak the reminder. |
| Speakers (`speakers`) | (empty) |  |
| Voice on/off switch (optional) (`speak_switch`) | (empty) | Pick an input_boolean or switch. The voice is only spoken while it is on; the phone push is not affected. Leave empty for always on. |
| Speak only while someone is home (optional) (`speak_presence`) | (empty) | Pick a person, a group or a binary sensor. The voice is only spoken while it is home or on, so the speaker stays quiet in an empty house. The phone push is not affected. Leave empty for always. |
| Tapping the push opens the Luftwächter panel (`open_panel`) | `False` | When on, a tap on the phone notification opens the sidebar panel at the room of the window (companion app). |
| Spoken text (`speak_text`) | `{{ message }}` | Use {{ message }}, {{ room }}, {{ window }} and {{ minutes }}. |

