# Changelog

Alle nennenswerten Änderungen an diesem Repo. Format: [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unreleased]

### Added
- **`klimaanlage-smart-control.yaml`**: Neuer Schalter `cool_adaptive_target_enabled` (Default `true`, backward compatible). Wenn aus, wird der eingestellte `cool_target_temp` IMMER verwendet — der adaptive Clamp gegen die Außentemperatur (`outdoor − cool_max_delta_t`) entfällt. Use-Case: bei 35 °C draußen wirklich auf 23 °C kühlen statt nur auf 28 °C.

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
