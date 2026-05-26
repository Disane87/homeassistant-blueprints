# 🌬️ Smart AC Automation

> Der ursprüngliche „all-in-one" AC-Blueprint mit Trigger-Sensor, Zeitfenster und vielen Optionen. **Wird perspektivisch durch [Klimaanlage Smart Control](klimaanlage-smart-control.md) abgelöst**, bleibt aber im Repo, damit bestehende Installationen weiterlaufen.

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-ac-automation.yaml)

## 🧐 Worum geht's?

Klima ein/aus auf Basis eines Trigger-Sensors (typisch: Außentemperatur), mit Zeitfenster, Wochentags-Maske und optionalem Window-Stop. Älteres, monolithischeres Design — die Inputs heißen anders als beim neuen Blueprint, die Logik ist weniger granular.

## ⚠️ Empfehlung

Bei Neu-Setups bitte **[Klimaanlage Smart Control](klimaanlage-smart-control.md)** nehmen. Dort ist Heizen + Kühlen, Anwesenheit, Raumpräsenz, Urlaub, adaptiver Target und Cycle-Schutz schon eingebaut.

## 📋 Inputs

Die Original-Inputs sind in der Blueprint-Datei selbst dokumentiert (`name:` und `description:` pro Input). Im HA-Frontend siehst du den gleichen Stand wie hier — am besten dort durchklicken.

## 🔗 Migration

Wenn du von hier zu „Klimaanlage Smart Control" wechselst:

1. Alte Automation **deaktivieren**, nicht löschen — als Fallback.
2. Neue Automation aus dem neuen Blueprint anlegen, gleiche Sensoren wählen.
3. Eine Woche parallel laufen lassen (alte deaktiviert), Verhalten beobachten.
4. Alte Automation löschen.
