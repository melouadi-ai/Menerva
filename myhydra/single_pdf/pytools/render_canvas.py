"""Genera la copia canvas dai file documentati (stesso AST, 1 spazio per livello).

Il canvas MyHydra non accetta `def`/`class`/`lambda` e ha un limite di paste:
le due copie (documentata con commenti, canvas senza) sono rimaste allineate a
mano fino al 28 ott 2026, quando `bit_offset_pagina` e' entrato in `src` ma non
nelle copie: la pagina 1-based sarebbe rimasta rotta sul canvas senza che i test
lo vedessero (i test di parita' confrontavano solo pytools vs pytools).

Uso:
    python myhydra/single_pdf/pytools/render_canvas.py           # verifica
    python myhydra/single_pdf/pytools/render_canvas.py --write   # riscrive

La verifica e' anche un test (`tests/test_single_consolidator_canvas.py`).
"""

import io
import sys
import tokenize
from pathlib import Path

HERE = Path(__file__).parent


def render(src_text):
    """Commenti via, righe vuote via, un solo spazio di indentazione per livello."""
    cut = {}
    depth_of_row = {}
    depth = 0
    for tok in tokenize.generate_tokens(io.StringIO(src_text).readline):
        if tok.type == tokenize.INDENT:
            depth += 1
        elif tok.type == tokenize.DEDENT:
            depth -= 1
        elif tok.type == tokenize.COMMENT:
            cut.setdefault(tok.start[0], tok.start[1])
        if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                        tokenize.DEDENT, tokenize.COMMENT,
                        tokenize.ENDMARKER):
            continue
        depth_of_row.setdefault(tok.start[0], depth)
    out = []
    for no, line in enumerate(src_text.splitlines(), 1):
        if no in cut:
            line = line[:cut[no]].rstrip()
        if not line.strip():
            continue
        out.append(" " * depth_of_row[no] + line.lstrip(" "))
    return _join_brackets("\n".join(out) + "\n")


def _join_brackets(text):
    """Unisce le righe spezzate dentro parentesi: solo formattazione.

    Ogni riga di continuazione costa indentazione (fino a 20 byte) che sul
    canvas non serve a niente: l'AST non cambia, il paste resta sotto soglia.
    """
    rows = text.splitlines()
    depth = {}
    level = 0
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.OP:
            if tok.string in "([{":
                level += 1
            elif tok.string in ")]}":
                level -= 1
        if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                            tokenize.DEDENT, tokenize.COMMENT,
                            tokenize.ENDMARKER):
            depth[tok.end[0]] = level
    out = []
    i = 0
    while i < len(rows):
        line = rows[i]
        while depth.get(i + 1, 0) > 0 and i + 1 < len(rows):
            i += 1
            line = line + " " + rows[i].lstrip()
        out.append(line)
        i += 1
    return "\n".join(out) + "\n"


PAIRS = [
    ("consolidator.py", "consolidator_canvas.py"),
    ("json_creator_v15.py", "json_creator_v15_canvas.py"),
]


def main(argv):
    write = "--write" in argv
    bad = 0
    for doc_name, canvas_name in PAIRS:
        doc = HERE / doc_name
        canvas = HERE / canvas_name
        want = render(doc.read_text(encoding="utf-8"))
        if write:
            canvas.write_text(want, encoding="utf-8")
            print("scritto", canvas.name, len(want.encode()), "byte")
            continue
        have = canvas.read_text(encoding="utf-8")
        same = have == want
        print("%-30s %s (%d byte)" % (canvas_name,
                                      "allineato" if same else "DIVERSO",
                                      len(have.encode())))
        bad += 0 if same else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
