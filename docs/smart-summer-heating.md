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

Inputs siehe Blueprint-Datei. Wichtigste:

- Außentemperatur-Sensor
- Schwellwert °C (Default: ~18 °C)
- Beobachtungszeitraum (z. B. 24h)
- Liste der `climate.*` Entities, die geschaltet werden sollen

## 🔗 Verwandt

- Mein anderer Heizungs-Blueprint: `heating_min_switchover.yaml` (im HA-Setup vorhanden, nicht im öffentlichen Repo, weil sehr Tado-spezifisch)
