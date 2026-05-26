# 🌡️ Klimaanlage Smart Control

> Vollautomatische Steuerung einer Split-Klimaanlage — Heizen **und** Kühlen, mit Fenster-, Anwesenheits- und Raumpräsenz-Logik, Urlaubsmodus, adaptivem Cooling-Target, Mindest-Cycle-Schutz und optionaler Fußbodenheizungs-Koordination. Das ist der Blueprint, den ich bei mir im Büro produktiv laufen habe.

[![Import](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FDisane87%2Fhomeassistant-blueprints%2Fblob%2Fmain%2Fklimaanlage-smart-control.yaml)

## 🧐 Wann brauche ich das?

Du hast eine Split-Klimaanlage (Hisense ConnectLife, Tuya, Daikin, was auch immer als `climate.*` in HA auftaucht) und willst sie nicht jeden Tag manuell ein- und ausschalten. Du willst:

- automatisches Kühlen, wenn es im Raum zu warm wird **und** draußen tatsächlich heiß ist (nicht im Mai bei 19 °C)
- automatisches Heizen, wenn es draußen kalt ist, aber nicht so kalt, dass die Wärmepumpe ineffizient wird (typisch −10 °C, je nach Gerät)
- ein **definitives Aus**, wenn das Fenster offen ist, niemand zuhause ist, der Raum leer ist oder du im Urlaub bist
- Koordination mit der Fußbodenheizung: läuft die Klima, schaltet das Thermostat aus, kommt die Klima wieder aus und es ist Heiz-Wetter, geht das Thermostat zurück auf `heat`

Genau das macht der Blueprint.

## 📋 Inputs

### Gerät & Sensoren

| Input | Default | Beschreibung |
|---|---|---|
| `climate_entity` | – | Die Klimaanlage als `climate.*` Entity. |
| `room_temp_sensor` | – | Temperatursensor im Raum (`device_class: temperature`). |
| `outdoor_temp_sensor` | `sensor.klima_wohnzimmer_wetter_garten_temperature` | Außentemperatur. Idealerweise ein eigener Sensor in der Verschattung. |

### Thermostat & Fenster

| Input | Default | Beschreibung |
|---|---|---|
| `thermostat_entity` | (leer) | Optionales `climate.*` Thermostat der Fußbodenheizung. Wird auf `off` gesetzt, wenn die Klima läuft, und auf `heat` zurückgesetzt, wenn sinnvoll. |
| `window_sensor` | (leer) | Optionaler Fenster-Kontakt. AC startet nicht bei offenem Fenster und schaltet sofort ab, falls geöffnet während Betrieb. |

### Anwesenheit

| Input | Default | Beschreibung |
|---|---|---|
| `presence_sensor` | `binary_sensor.family_presence` | Haus-Ebene: `on` = jemand zuhause, `off` = niemand. |
| `presence_required` | `true` | Wenn aus, ignoriert die Logik den Anwesenheitssensor. |
| `room_presence_sensor` | `binary_sensor.family_presence` | Raum-Ebene (z. B. mmWave/FP2/PIR). Default fällt auf den Hauspräsenzsensor zurück. |
| `room_presence_required` | `true` | Wenn aus, wird der Raumsensor ignoriert. |
| `room_presence_grace_minutes` | `10` | AC bleibt nach Verlassen des Raums noch X Minuten an, bevor abgeschaltet wird. Vermeidet ständiges An/Aus bei kurzer Abwesenheit (Klo, Küche). |

### Urlaub

| Input | Default | Beschreibung |
|---|---|---|
| `vacation_boolean` | `input_boolean.urlaub` | Ein `input_boolean` oder `binary_sensor` als Urlaubs-Schalter. |
| `vacation_required` | `true` | Wenn aus, wird der Urlaubsschalter ignoriert. |

### Selbstregelung

| Input | Default | Beschreibung |
|---|---|---|
| `self_regulate` | `true` | Wenn aktiv, schaltet die Automation **nicht** ab, wenn der Trigger-Threshold unterschritten wird, sondern lässt die Klima intern bis zur Zieltemperatur regeln. Fenster-offen und Anwesenheits-/Urlaubs-Checks bleiben aber aktiv (Sicherheit). |

### Zeitfenster

| Input | Default | Beschreibung |
|---|---|---|
| `time_start` | `07:00:00` | Frühester automatischer Start. |
| `time_end` | `22:00:00` | Spätester automatischer Start. Außerhalb wird aktiv ausgeschaltet. |

### Effizienz

| Input | Default | Beschreibung |
|---|---|---|
| `cool_adaptive_target_enabled` | `true` | Schaltet den adaptiven Cooling-Target an/aus. Aus = der eingestellte `cool_target_temp` wird IMMER verwendet, unabhängig von der Außentemperatur (bei 35 °C draußen wird wirklich auf z.B. 23 °C gekühlt). |
| `cool_max_delta_t` | `7.0` °C | Nur wirksam wenn `cool_adaptive_target_enabled = true`. Δ Innen−Außen wird beim Kühlen begrenzt. Bei 30 °C draußen und Δ=7 → effektiver Cooling-Target ≥ 23 °C. Schont Kompressor + Gesundheit, spart 15–25 %. |
| `min_cycle_minutes` | `5` min | Mindest-Pause nach AC-Aus, bevor sie wieder starten darf. Verhindert Kurztakten. |

### Kühlen

| Input | Default | Beschreibung |
|---|---|---|
| `cool_enabled` | `true` | Kühl-Logik global an/aus. |
| `cool_room_trigger` | `26.0` °C | Raumtemp.-Schwelle, ab der gekühlt wird. |
| `cool_outdoor_min` | `18.0` °C | Mindest-Außentemperatur, sonst lieber lüften. |
| `cool_target_temp` | `23.0` °C | Basis-Target. Kann durch `cool_max_delta_t` nach oben angehoben werden — aber nur wenn `cool_adaptive_target_enabled` aktiv ist. |
| `cool_hysteresis` | `1.5` °C | Aus bei Raumtemp. ≤ Effektiv-Target − Hysterese. |

### Heizen

| Input | Default | Beschreibung |
|---|---|---|
| `heat_enabled` | `true` | Heiz-Logik global an/aus. |
| `heat_room_trigger` | `18.0` °C | Raumtemp.-Schwelle, unter der geheizt wird. |
| `heat_outdoor_max` | `12.0` °C | Max. Außentemp., damit überhaupt geheizt wird. |
| `heat_outdoor_min` | `-10.0` °C | Untere Effizienzgrenze, darunter ist Fußbodenheizung sinnvoller. |
| `heat_target_temp` | `21.0` °C | Heiz-Ziel. |
| `heat_hysteresis` | `1.0` °C | Aus bei Raumtemp. ≥ Target + Hysterese. |

## 🧠 Logik im Detail

### Trigger

- Zustandsänderung Raumtemperatur (jede)
- Zustandsänderung Außentemperatur (jede)
- Time-Pattern alle 10 Minuten (Re-Evaluation, falls keine Zustandsänderung kommt)
- Fenster auf/zu
- Hausanwesenheit ändert sich
- Raumpräsenz: `on` sofort, `off` mit Grace-Periode
- Urlaubs-Schalter ändert sich
- HA-Start
- Automation-Reload
- `time_start` und `time_end`

### Sicherheits-Conditions (greifen IMMER zuerst)

1. **Urlaub aktiv** → Klima aus, Thermostat aus, fertig
2. **Fenster geöffnet** → Klima aus (Thermostat wird *nicht* wiederhergestellt, weil dann beim Lüften die Heizung ginge)
3. **Niemand zuhause oder Raum leer** → Klima aus
4. **Außerhalb Zeitfenster** → Klima aus, Thermostat ggf. zurück auf `heat`

### Hauptlogik

Erst danach kommt überhaupt die Frage *kühlen oder heizen*:

- **Kühlen,** wenn:
  `cool_enabled` ∧ kein Fenster auf ∧ Anwesenheit ok ∧ Außentemp ≥ Mindest ∧ Raumtemp ≥ Trigger
- **Heizen,** wenn:
  `heat_enabled` ∧ kein Fenster auf ∧ Anwesenheit ok ∧ Außentemp ≤ Obergrenze ∧ Außentemp ≥ Effizienzgrenze ∧ Raumtemp ≤ Trigger
- **Effektiver Cooling-Target:**
  - Wenn `cool_adaptive_target_enabled = true` (Default): `max(cool_target_temp, outdoor_temp − cool_max_delta_t)`
  - Wenn `cool_adaptive_target_enabled = false`: `cool_target_temp` (fest, ohne Außentemperatur-Clamp)
- **Cycle-Check:** Wenn der aktuelle Zustand der Klima `off` ist, prüft die Logik, wie lange das schon so ist. Erst nach `min_cycle_minutes` darf wieder gestartet werden.

### Fußbodenheizung

Sobald die Klima `cool` oder `heat` schaltet, geht das optional konfigurierte Thermostat auf `off`. Stoppt die Klima (Trigger weg, Hysterese erreicht **und** `self_regulate=false`), wird das Thermostat zurück auf `heat` gesetzt — aber nur wenn (a) Heizung gerade sinnvoll ist (`outdoor ≤ heat_outdoor_max`) und (b) das Fenster zu ist.

### Selbstregelung

Mit `self_regulate=true` (Default) hört die Automation auf zu schalten, sobald die Klima läuft. Sie lässt das Gerät selbst zur Zieltemperatur regeln. Erst Sicherheits-Events (Fenster, Anwesenheit, Urlaub, Zeitfenster-Ende) bringen die Klima wieder zum Aus. Das ist der bessere Modus für Geräte, die eine ordentliche Inverter-Regelung haben.

## 🏠 Mein konkretes Setup im Büro

```yaml
climate_entity: climate.klimaanlage_buro_marco_2
room_temp_sensor: sensor.klimasensor_buro_marco_temperature
outdoor_temp_sensor: sensor.klima_wohnzimmer_wetter_garten_temperature
thermostat_entity: climate.buro_marco        # Tado-Heizkörperthermostat
window_sensor: binary_sensor.fensterkontakt  # Aqara Fenster-Sensor
presence_sensor: binary_sensor.family_presence
presence_required: true
room_presence_sensor: binary_sensor.fp2_buro_marco_presence_any  # Aqara FP2
room_presence_required: true
room_presence_grace_minutes: 10
time_start: "07:00:00"
time_end: "22:00:00"
cool_enabled: true
cool_room_trigger: 23      # mir wird's früh warm im Büro
cool_outdoor_min: 18
cool_target_temp: 21
cool_hysteresis: 1.5
heat_enabled: true
heat_room_trigger: 18
heat_outdoor_max: 12
heat_outdoor_min: -10
heat_target_temp: 21
heat_hysteresis: 1
```

Das läuft seit Mai 2026 stabil bei mir. Der einzige manuelle Eingriff: einmal `input_boolean.urlaub` an, wenn wir wegfahren, und wieder aus, wenn wir zurück sind.

## ⚠️ Bekannte Edge-Cases

- **HA-Neustart mitten im Betrieb:** Der `last_changed` der Klima-Entity wird beim Neustart neu gesetzt. Direkt nach Neustart kann der Cycle-Schutz also fälschlich „Pause noch nicht abgelaufen" sagen. In der Praxis irrelevant (5 Minuten).
- **Fenster auf während Selbstregelung:** Wird **vor** der Selbstregelung geprüft. Klima geht aus. Beim Fenster zu startet sie erst beim nächsten regulären Trigger (10-Min-Pattern oder Temperaturänderung), nicht sofort. Das ist Absicht: einmal aus, einmal kurz durchlüften.
- **Mode `single`:** Wenn die Automation gerade läuft (z. B. wartet im `set_temperature`), wird ein paralleler Trigger verworfen (`max_exceeded: silent`). Bei einem 10-Sekunden-Action-Block ist das in der Praxis kein Problem.

## 🔗 Verwandt

- [Smart Entfeuchten](smart-dehumidify.md) — wenn du gleichzeitig Heat-Cool-Zyklus zum Entfeuchten brauchst
- Blog-Post zum Blueprint: [Klimaanlage Smart Control auf blog.disane.dev](https://blog.disane.dev/) *(Link wird beim Veröffentlichen aktualisiert)*
