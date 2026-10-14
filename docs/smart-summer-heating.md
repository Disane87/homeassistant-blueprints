# 🌞 Heizung Sommermodus (Smart)

> Schaltet Thermostate automatisch **aus**, wenn die Außentemperatur dauerhaft über einem Schwellwert bleibt. Sobald es wieder kühler wird, geht alles zurück auf `heat`.

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-summer-heating.yaml)

## 🧐 Worum geht's?

Heizkörper-Thermostate (Tado, AVM DECT, generische `climate.*`-Entities) ziehen im Sommer keinen Strom für Wärme, aber:

- die Pumpen-Logik der Therme läuft trotzdem oft an, weil ein Thermostat „kalt" meldet
- die Stellantriebe takten unnötig
- die Therme braucht ggf. einen Sommer-Modus, der manuell zu setzen wäre

Dieser Blueprint nimmt der Sache die Manuell-Arbeit ab: über einen Trend-Sensor wird beobachtet, wann es dauerhaft warm genug ist, und schaltet die ausgewählten Thermostate auf `off`. Bei Kälteeinbruch geht's wieder zurück.

## 📋 Inputs

| Input | Default | Beschreibung |
|---|---|---|
| `outdoor_temp_sensor` | – | Außentemperatursensor |
| `outdoor_temp_avg_sensor` | leer | Optional, empfohlen: gemittelter Sensor (z. B. Statistik-Helfer, Mittelwert 24h). Wenn gesetzt, wird er für die Entscheidung genutzt |
| `climate_targets` | – | Thermostate (Mehrfachauswahl) |
| `ac_targets` | leer | Klimaanlagen pro Raum (Mehrfachauswahl), werden wie Thermostate geschaltet, aber nicht von der Ventilübung erfasst |
| `summer_on_threshold` | 15 °C | Darüber: Geräte aus |
| `summer_off_threshold` | 12 °C | Darunter: Geräte wieder an |
| `check_interval_minutes` | 15 min | Zyklische Prüfung zusätzlich zu Sensoränderungen |
| `valve_exercise_*` | an, Mo 10:00, 10 min | Wöchentliche Ventilübung (nur im Sommermodus) |
| `notify_service` | leer | Optionaler Notify-Dienst |

## ⚙️ Logik

- **Kontinuierliche Prüfung:** bei jeder Änderung des Außensensors, zyklisch alle `check_interval_minutes` und beim HA-Start.
- Wert über `summer_on_threshold` → alle Geräte, die noch an sind, werden ausgeschaltet.
- Wert unter `summer_off_threshold` → alle Geräte, die aus sind, werden eingeschaltet.
- Dazwischen passiert nichts (Hysterese). Manuelle Eingriffe oder ein Heizprogramm werden beim nächsten Check korrigiert.

## ⚠️ Caveats

- Ohne Durchschnittssensor wird der aktuelle Wert verwendet. Bei großen Tag/Nacht-Schwankungen (> Hysterese) schaltet die Automation dann mehrfach täglich um. Ein 24h-Mittelwert-Sensor löst das.
- Der frühere Input `confirmation_hours` (`for:`-Trigger) ist entfallen. Er erforderte durchgehend 24 h über/unter dem Schwellwert und löste deshalb im Frühjahr/Herbst kaum aus. Automationen einmal neu speichern.
- Schaltet das Heizprogramm die Thermostate morgens wieder ein, werden sie beim nächsten Check wieder ausgeschaltet.

## 🔗 Verwandt

- Mein anderer Heizungs-Blueprint: `heating_min_switchover.yaml` (im HA-Setup vorhanden, nicht im öffentlichen Repo, weil sehr Tado-spezifisch)
