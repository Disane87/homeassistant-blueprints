# Robuster Manuell-Override (input_boolean-Latch)

Das Blueprint **Klimaanlage Smart Control** erkennt manuelle Eingriffe (UI / App /
Voice) standardmäßig über `climate.context.user_id`. Das ist fragil: Viele
Klima-Integrationen (z.B. **ConnectLife** / Hisense / AEG) pollen das Gerät im
Sekundentakt und überschreiben dabei den Context der Climate-Entity
(`user_id → none`). Dadurch verfällt `manual_override` nach wenigen Sekunden — und
außerhalb des Aktiv-Zeitfensters schaltet die Automation eine **manuell**
eingeschaltete Klimaanlage prompt wieder ab.

## Lösung

Der optionale Input **„Manuell-Override Helfer"** (`manual_boolean`) wertet
zusätzlich einen `input_boolean` aus. Wird dieser von einer kleinen externen
Automation gesetzt, sobald ein Mensch die Klimaanlage ändert, überlebt der
Override die Poll-Updates. `manual_override` ist dann wahr, solange entweder der
Context frisch ist **oder** der Helfer `on` ist.

## Setup

### 1. Helfer anlegen

Einstellungen → Geräte & Dienste → Helfer → **Schalter (input_boolean)**, z.B.
`input_boolean.klima_<raum>_manuell`. (Oder per YAML / Package.)

### 2. Helfer im Blueprint zuweisen

In der Blueprint-Automation den Input **„Manuell-Override Helfer"** auf den
angelegten `input_boolean` setzen.

### 3. Latch-Automation (setzen + zurücksetzen)

```yaml
# Latcht den manuellen Eingriff. Poll-Updates der Integration haben keine
# user_id und werden ignoriert.
- alias: "Klima <Raum> – Manuell-Override latchen"
  mode: single
  triggers:
    - trigger: state
      entity_id: climate.klimaanlage_<raum>
  conditions:
    - condition: template
      value_template: >-
        {{ trigger.to_state is not none
           and trigger.to_state.context.user_id is not none }}
  actions:
    - action: input_boolean.turn_on
      target:
        entity_id: input_boolean.klima_<raum>_manuell

# Hebt den Override zum Beginn des Aktiv-Zeitfensters auf (gleiche Uhrzeit wie
# der Input "Aktiv ab" / time_start des Blueprints), damit die Automation wieder
# die Kontrolle übernimmt.
- alias: "Klima <Raum> – Manuell-Override zurücksetzen"
  mode: single
  triggers:
    - trigger: time
      at: "19:00:00"
  actions:
    - action: input_boolean.turn_off
      target:
        entity_id: input_boolean.klima_<raum>_manuell
```

## Verhalten

- **Manuell EIN außerhalb des Zeitfensters** → bleibt an (Latch hält bis `time_start`).
- **Manuell AUS innerhalb des Zeitfensters** → Automation startet nicht erneut (Override respektiert auch manuelles Ausschalten).
- **Zum `time_start`** → Latch wird gelöscht, Automation übernimmt wieder.
- **Harte Safety-Overrides** (Urlaub, Fenster offen) greifen weiterhin unabhängig vom Latch.

> Leer lassen des Inputs = altes Verhalten (nur `context.user_id`). Voll
> abwärtskompatibel.
