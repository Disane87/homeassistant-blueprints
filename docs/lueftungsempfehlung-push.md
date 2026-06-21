# 💨 Lüftungsempfehlung Push

Schickt eine **Sammel-Push** aufs Handy „lüften ja/nein", sobald sich die
Empfehlung für deine Räume ändert — gegen **Feuchtigkeit / Schimmel** und im
**Sommer gegen Hitze**. Eine Benachrichtigung, alle betroffenen Räume:
`💨 Lüften empfohlen` → `• Schlafzimmer — kühlt & entfeuchtet (~10 min)`.

## Wann brauchst du das?

Du willst nicht selbst raten, ob Fensteröffnen gerade etwas bringt. Lüften
hilft nur, wenn die **Außenluft trockener** (entfeuchtet, Schimmelschutz)
und/oder **kühler** (Sommer-Hitze) ist als die Raumluft — sonst machst du es
schlimmer. Dieser Blueprint sagt dir genau das, pro Raum, push-basiert.

## 🧩 Architektur: zwei Teile

```
[Raum- & Außen-Sensoren]  →  sensor.luftungsempfehlung  →  dieser Blueprint  →  📱 Push
        (Daten)                  (Logik, Template)            (Zustellung)
```

1. **Template-Sensor** `sensor.luftungsempfehlung` — bewertet jeden Raum gegen
   die Außenluft (Garten) und fasst alle Empfehlungen in **einem** Entity
   zusammen. Komplettes YAML siehe unten.
2. **Dieser Blueprint** — triggert auf den Wechsel des `signatur`-Attributs,
   entprellt, prüft Ruhezeiten und schickt die fertige Sammel-Push.

Der Blueprint ist bewusst generisch: jeder Sensor mit `state` = Anzahl,
Attribut `signatur` (Änderungserkennung) und Attribut `text` (Push-Text)
funktioniert.

## ⚙️ Inputs

| Input | Default | Beschreibung |
|---|---|---|
| **Empfehlungs-Sensor** | – | Template-Sensor mit State=Anzahl, Attr. `signatur` + `text`. Standard: `sensor.luftungsempfehlung` |
| **Änderungs-Attribut** | `signatur` | Attribut, dessen Wechsel die Push auslöst |
| **Text-Attribut** | `text` | Attribut mit dem fertigen Push-Text |
| **Notify-Service** | `notify.notify` | Voller Service-Name, z. B. `notify.mobile_app_iphone_marco` |
| **Titel** | `💨 Lüften empfohlen` | Push-Titel |
| **Dashboard-Pfad** | `/lovelace-0/0` | Lovelace-Pfad, der beim Tippen geöffnet wird |
| **Entprellung (Minuten)** | `5` | Empfehlung muss so lange stabil sein, bevor gepusht wird |
| **Ruhezeit Ende** | `06:30` | Ab wann Pushes erlaubt sind |
| **Ruhezeit Beginn** | `22:30` | Ab wann keine Pushes mehr kommen |

## 🔁 Logik

**Trigger:** State-Change auf dem `signatur`-Attribut des Empfehlungs-Sensors,
entprellt über `for: <Entprellung>`.

**Conditions (Sicherheits-Checks zuerst):**

- State > 0 → es gibt überhaupt etwas zu lüften
- aktuelle Zeit liegt **außerhalb** der Ruhezeit

**Aktion:** Eine Push über den Notify-Service mit Titel + `text`-Attribut.
`tag`/`channel` sind fix gesetzt, sodass eine neue Empfehlung die vorige
**ersetzt** statt zu stapeln; `url`/`clickAction` öffnet das Dashboard.

## 🧮 Der Companion-Sensor `sensor.luftungsempfehlung`

Lege diesen trigger-basierten Template-Sensor in deiner `templates.yaml`
(oder via UI-Helfer/Template-Integration) an und passe die **Raumtabelle**
sowie die **Außen-Referenz** an deine Entities an.

Bewertung je Raum (Außenluft = Garten):

- `dah = AH_raum − AH_garten` (absolute Feuchte, g/m³) → positiv = außen trockener
- `dt  = T_raum − T_garten` (K) → positiv = außen kühler
- **entfeuchten** lohnt: `dah ≥ 0.5`
- **kühlen** lohnt: `T_raum ≥ 23 °C` **und** `dt ≥ 1 K`
- **schadet_hitze**: `T_raum ≥ 23 °C` **und** Garten wärmer als Raum
- Empfehlung: `entf & kühl` → „kühlt & entfeuchtet" · `entf & !schadet_hitze`
  → „entfeuchten" · `kühl` → „kühlen" (Hitze hat Priorität, auch wenn minimal
  Feuchte reinkommt) · sonst keine.
- Dauer aus `dah`: <1 → ~3 min · 1–3 → ~5 min · 3–5 → ~10 min · >5 → ~15 min
  (reines Kühlen: ~10 min).

```yaml
# templates.yaml
- trigger:
    - trigger: homeassistant
      event: start
    - trigger: time_pattern
      minutes: /5
    - trigger: state
      entity_id:
        # Außen-Referenz
        - sensor.garten_absolute_humidity
        - sensor.klima_wohnzimmer_wetter_garten_temperature
        # je Raum: Temperatur + absolute Feuchte
        - sensor.klima_wohnzimmer_temperature
        - sensor.thermal_comfort_wohnzimmer_absolute_humidity
        - sensor.klimasensor_schlafzimmer_temperature
        - sensor.schlafzimmer_absolute_humidity
        # ... weitere Räume ergänzen ...
  variables:
    result: >-
      {% set ah_out = states('sensor.garten_absolute_humidity') | float(-99) %}
      {% set t_out  = states('sensor.klima_wohnzimmer_wetter_garten_temperature') | float(-99) %}
      {% set ah_min = 0.5 %}
      {% set warm = 23.0 %}
      {% set t_margin = 1.0 %}
      {% set rooms = [
        {'key':'Wohnzimmer','t':'sensor.klima_wohnzimmer_temperature','ah':'sensor.thermal_comfort_wohnzimmer_absolute_humidity'},
        {'key':'Schlafzimmer','t':'sensor.klimasensor_schlafzimmer_temperature','ah':'sensor.schlafzimmer_absolute_humidity'}
      ] %}
      {% set ns = namespace(out=[]) %}
      {% if ah_out > -90 and t_out > -90 %}
      {% for r in rooms %}
        {% set ah_in = states(r.ah) | float(-99) %}
        {% set t_in  = states(r.t)  | float(-99) %}
        {% if ah_in > -90 and t_in > -90 %}
          {% set dah = ah_in - ah_out %}
          {% set dt  = t_in - t_out %}
          {% set entf = dah >= ah_min %}
          {% set kuehl = (t_in >= warm) and (dt >= t_margin) %}
          {% set schadet_hitze = (t_in >= warm) and (t_out > t_in) %}
          {% set modus = '' %}
          {% if entf and kuehl %}
            {% set modus = 'kühlt & entfeuchtet' %}
          {% elif entf and not schadet_hitze %}
            {% set modus = 'entfeuchten' %}
          {% elif kuehl %}
            {% set modus = 'kühlen' %}
          {% endif %}
          {% if modus != '' %}
            {% if entf %}
              {% if dah < 1 %}{% set dauer = '~3 min' %}
              {% elif dah < 3 %}{% set dauer = '~5 min' %}
              {% elif dah < 5 %}{% set dauer = '~10 min' %}
              {% else %}{% set dauer = '~15 min' %}{% endif %}
            {% else %}
              {% set dauer = '~10 min' %}
            {% endif %}
            {% set ns.out = ns.out + [ {'key': r.key, 'modus': modus, 'dauer': dauer} ] %}
          {% endif %}
        {% endif %}
      {% endfor %}
      {% endif %}
      {{ ns.out }}
  sensor:
    - name: "Lüftungsempfehlung"
      unique_id: lueftungsempfehlung
      state: "{{ result | count }}"
      icon: >-
        {{ 'mdi:weather-windy' if (result | count) > 0 else 'mdi:window-closed-variant' }}
      attributes:
        anzahl: "{{ result | count }}"
        signatur: "{{ result | map(attribute='key') | list | sort | join('|') }}"
        raeume: "{{ result }}"
        text: >-
          {% if result | count == 0 %}
          Aktuell kein Lüften nötig.
          {% else %}
          {% set lines = namespace(l=[]) %}
          {% for r in result %}
          {% set lines.l = lines.l + ['• ' ~ r.key ~ ' — ' ~ r.modus ~ ' (' ~ r.dauer ~ ')'] %}
          {% endfor %}
          {{ lines.l | join('\n') }}
          {% endif %}
```

> 💡 Du hast keine `*_absolute_humidity`-Sensoren? Die liefert die
> [Thermal Comfort](https://github.com/dolezsa/thermal_comfort)-Integration
> pro Raum aus Temperatur + relativer Feuchte. Alternativ kannst du absolute
> Feuchte per Magnus-Formel im Template berechnen (siehe `smart-dehumidify.yaml`).

## 🏠 Beispiel-Setup (mein Zuhause)

10 Räume mit je einem Klimasensor (Temp + rel. Feuchte) → Thermal-Comfort
liefert `*_absolute_humidity`. Außen-Referenz ist die Gartenwetterstation
(`sensor.garten_absolute_humidity` + `…_garten_temperature`). Push geht über
`notify.notify` an die Familien-iPhones; Tap öffnet das Luftqualitäts-Dashboard
(`/lovelace-verbrauch/8`). Ruhezeit 22:30–06:30, Entprellung 5 min.

## ⚠️ Edge-Cases & Caveats

- **Nach `template.reload`** rechnet der trigger-basierte Sensor erst beim
  nächsten Trigger neu — die echten Klimasensoren updaten aber im Minutentakt
  von selbst, der `time_pattern: /5` ist zusätzlicher Fallback.
- **Keine „Entwarnung":** Sinkt die Empfehlung auf 0 Räume, kommt bewusst
  **keine** Push (State > 0 ist Bedingung). So bleibt es ruhig.
- **`signatur` statt State als Trigger:** Würde man nur auf den State (Anzahl)
  triggern, bliebe ein Wechsel von `{A}` → `{B}` (beide Anzahl 1) unbemerkt.
  Die `signatur` (sortierte Raum-Keys) fängt jede Mengen-Änderung.
- **Ruhezeit überspannt Mitternacht:** `condition: time` mit `after: 06:30`,
  `before: 22:30` erlaubt Pushes tagsüber — passt für die Default-Ruhezeit.
- **Absolute statt relativer Feuchte** ist Absicht: nur die absolute Feuchte
  (g/m³) sagt korrekt, ob Lüften tatsächlich Wasser aus dem Raum trägt.
