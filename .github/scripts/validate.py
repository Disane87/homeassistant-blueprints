"""Validate all blueprint YAML files at repo root.

Checks:
- Loads as YAML without errors
- Has top-level `blueprint` key
- `blueprint.name`, `blueprint.domain`, `blueprint.input` present
- `blueprint.domain == "automation"`
- No tab characters

Exits non-zero on first failure (CI gate).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml


class HAInput(str):
    """Placeholder for `!input <name>` references inside a blueprint."""


def _input_constructor(loader: yaml.Loader, node: yaml.Node) -> HAInput:
    return HAInput(loader.construct_scalar(node))


yaml.SafeLoader.add_constructor("!input", _input_constructor)

ROOT = Path(__file__).resolve().parents[2]
ERRORS: list[str] = []


def check(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "\t" in text:
        ERRORS.append(f"{path.name}: enthält Tab-Zeichen")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        ERRORS.append(f"{path.name}: YAML-Fehler — {exc}")
        return
    if not isinstance(data, dict) or "blueprint" not in data:
        ERRORS.append(f"{path.name}: kein `blueprint:`-Block am Root")
        return
    bp = data["blueprint"]
    for key in ("name", "domain", "input"):
        if key not in bp:
            ERRORS.append(f"{path.name}: `blueprint.{key}` fehlt")
    if bp.get("domain") != "automation":
        ERRORS.append(f"{path.name}: `blueprint.domain` muss `automation` sein (ist `{bp.get('domain')}`)")


def main() -> int:
    yamls = sorted(ROOT.glob("*.yaml"))
    if not yamls:
        print("Keine Blueprint-YAMLs gefunden — Repo leer?")
        return 1
    print(f"Validiere {len(yamls)} Blueprint(s)…")
    for path in yamls:
        check(path)
        print(f"  • {path.name}")
    if ERRORS:
        print("\n❌ Validierung fehlgeschlagen:")
        for err in ERRORS:
            print(f"  - {err}")
        return 1
    print("\n✅ Alle Blueprints sind valide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
