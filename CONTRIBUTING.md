# Contributing

Schön, dass du beitragen willst! 🙌 Damit die Blueprints konsistent und wartbar bleiben, hier ein paar Spielregeln.

## 🐛 Bug melden

Bitte ein [Bug-Issue](https://github.com/Disane87/homeassistant-blueprints/issues/new?template=bug_report.yml) aufmachen mit:

- Welcher Blueprint, welche HA-Version
- Erwartetes vs. tatsächliches Verhalten
- `automation.yaml`-Auszug (Inputs anonymisiert reicht)
- HA-Logs zum Zeitpunkt des Triggers (`Einstellungen → System → Protokolle`)
- Trace der Automation, falls verfügbar (`Automatisierungen → … → Spuren`)

## 💡 Feature vorschlagen

[Feature-Issue](https://github.com/Disane87/homeassistant-blueprints/issues/new?template=feature_request.yml) mit dem konkreten Use-Case. „Wäre cool wenn man X kann" reicht nicht — beschreib das **Szenario**, dann kann ich entscheiden, ob das in den bestehenden Blueprint passt oder einen neuen rechtfertigt.

## 🔧 Code beisteuern

1. Fork das Repo
2. Branch nach Schema `fix/<thema>` oder `feat/<thema>` (z. B. `feat/klima-luftqualitaet-sensor`)
3. Änderungen committen, Commit-Message im [Conventional-Commits](https://www.conventionalcommits.org/de/v1.0.0/)-Stil:
   - `feat(klimaanlage): adaptiver Heiz-Target nach Außentemp.`
   - `fix(dehumidify): Cycle-Counter überlebt HA-Neustart`
   - `docs(readme): Import-Badge aktualisiert`
4. **Lokale Validierung laufen lassen:**
   ```bash
   python .github/scripts/validate.py
   ```
5. PR aufmachen — die GitHub-Actions-Pipeline muss grün sein
6. In der PR-Beschreibung den Bezug zum Issue erwähnen (`Fixes #42`)

## 📐 Stil-Konventionen

- **Sprache der Inputs:** Deutsch (das ist mein primärer Use-Case). PRs mit zusätzlichen englischen `name`/`description` für die internationale Community sind aber willkommen.
- **Selectors konkret typisieren.** `entity` mit `domain` + `device_class`, nicht `entity` ohne Einschränkung.
- **Defaults sinnvoll setzen.** Lieber ein konservativer Default (kühlen ab 26 °C) als ein leerer Input.
- **Sicherheits-Checks immer am Anfang der Action.** Erst `is_vacation`, `window_open`, `no_presence` prüfen, dann erst die eigentliche Logik.
- **Templates lesbar.** Kurze Bedingungen inline, komplexe Logik in benannte Variablen (`want_cool`, `cycle_ready`, …).

## 📚 Doku

Jeder neue Blueprint braucht eine Datei in `docs/<name>.md` mit:

- Einleitung (was macht der Blueprint, wann brauchst du den)
- Tabelle aller Inputs (Name, Default, Beschreibung)
- Logik-Übersicht (Trigger, Conditions, Aktions-Zweige)
- Beispiel-Setup (z. B. „mein Büro bei mir zuhause")
- Bekannte Edge-Cases / Caveats

## 🧪 Test-Setup empfohlen

Da Blueprints ohne echte Geräte schwer zu testen sind, hilft eine Test-Automation mit Helfern (`input_number` als Fake-Sensor, `input_boolean` als Fake-Schalter), um die Logik durchzuspielen, bevor du sie an die echte Klimaanlage hängst.

## ❤️ Danke

Wenn du es bis hier gelesen hast: top. Falls etwas unklar ist, einfach ein Issue mit `question`-Label aufmachen, ich antworte normalerweise innerhalb von ein paar Tagen.
