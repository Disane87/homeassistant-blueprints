# 🏠 Home Assistant Blueprints — disane edition

> Eine Sammlung von Home-Assistant-Blueprints, die ich in meinem eigenen Smarthome produktiv einsetze. Alle Blueprints sind defensiv gebaut (Fenster auf → AC aus, niemand zuhause → AC aus, Sensor fällt aus → keine Schaltfehler) und über den HA-eigenen Import-Button mit einem Klick einsatzbereit.

Nichts hier ist „mal eben zusammengeklickt". Jeder Blueprint hat einen konkreten Anwendungsfall, läuft bei mir im Alltag und ist über mehrere Iterationen optimiert worden, weil Dinge eben am Anfang nie auf Anhieb so funktionieren wie man sich das vorstellt. 😄

---

## 📚 Inhalt

| Blueprint | Worum geht's | Doku | Import |
|---|---|---|---|
| **Klimaanlage Smart Control** | Vollautomatische Steuerung einer Split-Klimaanlage (Heizen + Kühlen) mit Fenster-, Anwesenheits- und Raumpräsenz-Logik, Urlaubsmodus, adaptivem Target, Mindest-Cycle-Schutz und Fußbodenheizungs-Koordination. | [docs/klimaanlage-smart-control.md](docs/klimaanlage-smart-control.md) | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fklimaanlage-smart-control.yaml) |
| **Smart AC Automation** | Älterer, monolithischer AC-Blueprint mit Trigger-Sensor + Zeitfenster. *Wird durch „Klimaanlage Smart Control" abgelöst, bleibt aber für Bestandsnutzer drin.* | [docs/smart-ac-automation.md](docs/smart-ac-automation.md) | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-ac-automation.yaml) |
| **Smart Entfeuchten** | Heat-Cool-Zyklus für die Klimaanlage, um den Raum gezielt zu entfeuchten, ohne dauerhaft zu kühlen. | [docs/smart-dehumidify.md](docs/smart-dehumidify.md) | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-dehumidify.yaml) |
| **Heizung Sommermodus** | Schaltet Thermostate automatisch aus, wenn die Außentemperatur dauerhaft über einem Schwellwert bleibt. | [docs/smart-summer-heating.md](docs/smart-summer-heating.md) | [![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fsmart-summer-heating.yaml) |

---

## 🚀 Schnellstart

1. **Im Home-Assistant-Frontend:** Klick auf den `Import Blueprint` Badge oben → HA öffnet den Import-Dialog mit der richtigen URL vorausgefüllt.
2. **Per CLI:** Datei in `<config>/blueprints/automation/Disane87/` ablegen, dann in HA `Einstellungen → Automatisierungen → Blueprints → Neu laden`.
3. **Automatisierung anlegen:** `Einstellungen → Automatisierungen → Erstellen → Aus Blueprint`, Inputs ausfüllen, speichern.

Jeder Blueprint hat eine ausführliche Doku unter `docs/`, inkl. Erklärung **aller** Inputs, der Entscheidungslogik und meinem konkreten Setup als Beispiel.

---

## 🧱 Designprinzipien

Alle Blueprints in diesem Repo folgen dem gleichen Bauplan, damit ich (und du) sie zuverlässig kombinieren kannst:

- **Sicherheit zuerst.** Fenster auf, niemand zuhause, Urlaub aktiv, Sensor `unavailable`: die Automation lässt das Gerät in Ruhe (oder schaltet aktiv aus). Lieber einmal zu oft nicht starten als einmal sinnlos den Kompressor takten.
- **Hysterese statt Schaltgewitter.** Ein- und Ausschaltgrenzen liegen nie auf demselben Wert. Sonst klackert die Klima alle 30 Sekunden.
- **Mindest-Cycle.** Kompressoren mögen keine Kurztakte. Nach dem Aus mindestens N Minuten Pause.
- **Selbstregelung optional.** Wer der internen Klima-Regelung vertraut, lässt die Automation nur EIN-/AUSschalten und die Klima selbst die Zieltemperatur halten.
- **Adaptive Targets.** Bei 32 °C draußen ist 18 °C drinnen weder gesund noch effizient. Der adaptive Cooling-Target sorgt dafür, dass das Δ zwischen Außen und Innen einen konfigurierbaren Maximalwert nicht überschreitet.
- **Domain-Sprache.** Inputs heißen so, wie ein menschlicher Bediener sie nennen würde: „Aktiv ab", „Raumtemp. Einschaltgrenze", „Anwesenheit erforderlich". Nicht `bool_param_7`.

---

## 🧪 Validierung

Jeder Commit wird durch einen GitHub-Actions-Workflow ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)) geprüft:

- YAML-Syntax (PyYAML)
- Pflichtfelder (`blueprint.name`, `blueprint.domain`, `blueprint.input`)
- `domain: automation` korrekt gesetzt
- Keine Tabs

Lokal:

```bash
python .github/scripts/validate.py
```

---

## 🤝 Mitmachen

PRs sind willkommen, vor allem für:

- Bugfixes (Edge Cases, die ich nicht getriggert habe)
- Übersetzungen (englische Inputs/Descriptions für die internationale Community)
- Neue Blueprints, die zum „defensiv + dokumentiert"-Stil passen

Details in [CONTRIBUTING.md](CONTRIBUTING.md). Bei Fragen oder Problemen: [Issue aufmachen](https://github.com/Disane87/homeassistant-blueprints/issues/new/choose), gerne mit den HA-Logs und der `automation.yaml` deiner Instanz (Inputs anonymisiert).

---

## 📋 Changelog

Versionierter Verlauf in [CHANGELOG.md](CHANGELOG.md). Format: [Keep a Changelog](https://keepachangelog.com/).

---

## 📜 Lizenz

[MIT](LICENSE) — mach damit, was du willst. Wenn dir was hilft oder kaputtgeht, freue ich mich über einen kurzen Hinweis: [blog.disane.dev](https://blog.disane.dev) oder [@disane auf GitHub](https://github.com/Disane87).

---

## 🔗 Verwandt

- 📝 Blog: [blog.disane.dev](https://blog.disane.dev) — Tutorials, Reviews, Home-Lab-Notizen
- 🏡 HA-Config-Backup: [Disane87/homeassistant-config](https://github.com/Disane87/homeassistant-config) *(privat, aber zeigt den Stack als Ganzes)*
- 🛠 Mein anderer HA-Kram: [Disane87/spoolman-homeassistant](https://github.com/Disane87/spoolman-homeassistant), [Disane87/esphome-ha-eink](https://github.com/Disane87/esphome-ha-eink)
