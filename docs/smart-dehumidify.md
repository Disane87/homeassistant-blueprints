# 💧 Smart Entfeuchten via Klimaanlage (Heat-Cool-Zyklus) [v2.1]

> Entfeuchtet einen Raum gezielt, indem die Klimaanlage abwechselnd kühlt und heizt (Heat-Cool-Zyklus). Effektiver als reine Dehumidify-Modi vieler Geräte, weil die Klima dabei tatsächlich Wasser aus der Luft kondensieren lässt.

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-dehumidify.yaml)

## 🧐 Worum geht's?

Viele Split-Klimas haben einen „Dry"-Modus, der in der Praxis aber oft nur den Lüfter laufen lässt und kaum entfeuchtet. Dieser Blueprint nimmt die Sache selbst in die Hand: er fährt einen **Cool-Zyklus** (Wasser kondensiert am Wärmetauscher) und danach einen kurzen **Heat-Zyklus**, um den Raum nicht auszukühlen.

## 📋 Inputs

Inputs siehe Blueprint-Datei (`name:`/`description:` im HA-Frontend). Wichtigste Parameter:

- Luftfeuchte-Sensor + Zielwert
- Cool-Dauer pro Zyklus
- Heat-Dauer pro Zyklus
- Maximale Anzahl Zyklen
- Hysterese auf Luftfeuchte

## 🔗 Verwandt

- [Klimaanlage Smart Control](klimaanlage-smart-control.md) — für reguläres Heizen/Kühlen
