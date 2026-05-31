# Changelog

Alle nennenswerten Änderungen an diesem Repo. Format: [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unreleased]

### Added
- **`klimaanlage-smart-control.yaml`**: Neuer Schalter `cool_adaptive_target_enabled` (Default `true`, backward compatible). Wenn aus, wird der eingestellte `cool_target_temp` IMMER verwendet — der adaptive Clamp gegen die Außentemperatur (`outdoor − cool_max_delta_t`) entfällt. Use-Case: bei 35 °C draußen wirklich auf 23 °C kühlen statt nur auf 28 °C.
- **`klimaanlage-smart-control.yaml`**: Neue Section **„Modi (Eco / Super / Sleep)"** mit drei optionalen, zeit-/wochentag-basierten Phasen — alle Inputs leer lassen = Verhalten unverändert (backward compatible):
  - **Eco-Phase** (`eco_switch`, `eco_enabled`, `eco_time_start`, `eco_time_end`): schaltet einen Eco-Switch der Klimaanlage im konfigurierten Zeitfenster automatisch ein/aus. Geht die AC aus (Fenster/Urlaub/no_presence/time_end), wird Eco ebenfalls deaktiviert.
  - **Super-/Boost-Phase** (`super_switch`, `boost_enabled`, `boost_minutes`): aktiviert den Turbo-Switch für X Minuten ab dem automatischen Cool-Start, damit der Raum schnell auf Zieltemperatur kommt. Danach automatisch wieder aus.
  - **Sleep-Phase** (`sleep_select`, `sleep_enabled`, `sleep_profile`, `sleep_time_start`, `sleep_time_end`): setzt eine Sleep-Mode-Select-Entity auf das gewählte Profil (`general`/`for_old`/`for_young`/`for_kid`) im Zeitfenster und auf `off` außerhalb.
  - **`modi_weekdays`**: Multi-Select-Filter, an welchen Wochentagen Eco-Phase und Sleep-Phase aktiv sind. Default: alle 7 Tage.
- **`klimaanlage-smart-control.yaml`**: **Manual-Override-Erkennung** via `context.user_id`. Sobald die AC manuell per UI/App/Voice-Assistant verändert wird, überspringt die Automation für den Rest des heutigen Aktiv-Zeitfensters ihre proaktiven Aktionen (cool/heat start, time_end-off, no_presence-off, Modi-Toggles). **Safety-Overrides bleiben aktiv:** Urlaubsmodus und „Fenster offen" schalten weiterhin zwingend ab. Reset passiert automatisch am nächsten `time_start`.

### Changed
- **`klimaanlage-smart-control.yaml`**: Defaults für privatpersonenbezogene Entity-IDs entfernt (`binary_sensor.family_presence`, `input_boolean.urlaub`, `sensor.klima_wohnzimmer_wetter_garten_temperature`) — alle Sensor-Felder sind jetzt sauber leer und müssen vom Nutzer aktiv gewählt werden.

## [2026-05-26] — Klimaanlage Smart Control Release 🎉

### Added
- **`klimaanlage-smart-control.yaml`** — neuer Blueprint, der `smart-ac-automation.yaml` perspektivisch ablöst:
  - Heizen **und** Kühlen in einer Automation
  - Anwesenheits- + Raumpräsenz-Logik (Haus-Ebene + Raum-Ebene, mit Nachlaufzeit)
  - Urlaubsmodus über `input_boolean`
  - Adaptiver Cooling-Target (Δ Innen−Außen wird begrenzt)
  - Mindest-Cycle nach Aus (Kompressor-Schutz)
  - Selbstregelung: Klima darf intern eigenständig zur Zieltemperatur regeln
  - Fußbodenheizung wird beim AC-Start abgeschaltet und beim AC-Stopp koordiniert zurückgeschaltet
- Komplettes Repo-Setup: README, LICENSE, CONTRIBUTING, CHANGELOG, Issue-/PR-Templates, GitHub-Actions-Validierung
- `docs/`-Verzeichnis mit Detail-Doku pro Blueprint

### Changed
- Repo-Layout um `docs/` und `.github/` erweitert. YAML-Dateien bleiben am Root, damit die HA-Import-URLs aller Bestandsnutzer weiter funktionieren.

## [2026-04-10] — Initial Public

### Added
- `smart-ac-automation.yaml` — initialer AC-Blueprint
- `smart-dehumidify.yaml` — Heat-Cool-Zyklus zum Entfeuchten
- `smart-summer-heating.yaml` — Heizung-Sommer-Abschaltung
