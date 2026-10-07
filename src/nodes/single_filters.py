"""LV1 row filters for the Single PDF flow (prompt v14 rules V2/V20/V21).

Pure, testable logic. The canvas pytools later inline this code; the
``zona`` field is read ONLY to decide the V21 skip, never as a
name, group or description.
"""

from typing import Mapping, Optional, Tuple

# V2: exact-match discards (compared case-insensitively after strip).
_V2_SPARE = frozenset({
    "disponibile",
    "disponibile/",
    "disponible",
    "riserva",
    "spare",
    "reserve",
    "non utilizzato",
    "non utilizzata",
    "non usato",
    "libero",
    "---",
})

# V2: exact-match section headers (compared case-insensitively after strip).
_V2_HEADERS = frozenset({
    "misure",
    "comandi",
    "impostazioni",
    "input",
    "output",
    "parametri",
    "registri",
    "segnali",
    "variabili",
    "allarmi",
    "stati",
})

# V20: substring discards on the annotation/note (compared case-insensitively).
_V20_PHRASES = (
    "no pc sme",
    "no sme",
    "not used",
    "non utilizzato",
)

# Keys scanned for the V20 annotation (trailing text after the last column
# may arrive under any of these names; the v14 variable schema has no
# dedicated note field).
_NOTE_KEYS = (
    "note",
    "nota",
    "notes",
    "annotation",
    "annotazione",
    "comment",
    "commento",
    "trailing_note",
)


def _normalize_text(value: object) -> str:
    """Strip, collapse inner whitespace and lowercase for comparisons."""
    return " ".join(str(value).strip().split()).lower()


def _read_note(row: Mapping) -> str:
    """Return the first non-empty annotation found, else an empty string."""
    get = getattr(row, "get", None)
    if get is None:
        return ""
    for key in _NOTE_KEYS:
        try:
            value = get(key)
        except Exception:
            continue
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _read_zona(row: Mapping) -> Optional[str]:
    """Return the zona/area value, else None. Used ONLY for the V21 skip."""
    get = getattr(row, "get", None)
    if get is None:
        return None
    for key in ("zona", "area", "ZONA", "AREA"):
        try:
            value = get(key)
        except Exception:
            continue
        if isinstance(value, str) and value.strip():
            return value
    return None


def classify_row_with_reason(row: Mapping) -> Tuple[str, Optional[str]]:
    """Classify one v14 variable row.

    Returns a ``(decision, reason)`` pair where ``decision`` is one of
    ``"keep"``, ``"V2"``, ``"V20"`` or ``"V21"`` and ``reason`` is a short
    human-readable motive (None for ``"keep"``).

    Precedence when several rules match: V2 > V21 > V20. Every discard
    carries its rule code so discards are counted, never silent.
    """
    get = getattr(row, "get", None)
    raw_description = get("description") if get else None

    # V2: empty description.
    if raw_description is None:
        return ("V2", "description is null")
    if not isinstance(raw_description, str):
        return ("keep", None)
    if not raw_description.strip() or raw_description.strip() == "/":
        return ("V2", "description is empty or '/'")

    normalized = _normalize_text(raw_description)
    if normalized in _V2_SPARE:
        return ("V2", "description is a spare/placeholder token: %r" % raw_description.strip())
    if normalized in _V2_HEADERS:
        return ("V2", "description is a section header: %r" % raw_description.strip())
    # Anything merely CONTAINING those words is kept.

    # V21: hardware zone. The value is only tested, never reused as a name.
    zona = _read_zona(row)
    if zona is not None:
        zone_key = " ".join(zona.strip().split()).upper()
        if "INPUT_HW" in zone_key or "OUTPUT_HW" in zone_key or zone_key.endswith("_HW"):
            return ("V21", "zona is a hardware zone: %r" % zona.strip())

    # V20: exclusion annotation on the row.
    note = _read_note(row)
    if note:
        lowered = " ".join(note.strip().split()).lower()
        for phrase in _V20_PHRASES:
            if phrase in lowered:
                return ("V20", "annotation contains %r" % phrase.upper())

    return ("keep", None)


def classify_row(row: Mapping) -> str:
    """Return ``"keep"`` or the discarding rule code (``"V2"``/``"V20"``/``"V21"``)."""
    decision, _ = classify_row_with_reason(row)
    return decision
