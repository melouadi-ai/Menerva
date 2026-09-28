import json
import re

input_json = r'''{edge}[11]'''

input_json = input_json.replace("```json", "").replace("```", "").strip()

data = json.loads(input_json)

for station in data:

    # Raccogli i NAME delle misure per controllo duplicati
    all_measure_names = [m["NAME"] for m in station.get("measures", []) if m.get("NAME") is not None]

    # Calcola le basi (nomi senza parentesi) per trovare i duplicati
    bases = []
    for n in all_measure_names:
        s = n
        prev = None
        while prev != s:
            prev = s
            s = re.sub(r'\([^()]*\)', '', s)
        prev = None
        while prev != s:
            prev = s
            s = re.sub(r'\[[^\[\]]*\]', '', s)
        s = s.replace('"', '').replace("'", '')
        s = re.sub(r' {2,}', ' ', s).strip()
        bases.append(s)

    for i, m in enumerate(station.get("measures", [])):
        if m["NAME"] is not None:
            s = m["NAME"]
            base = bases[i]
            has_duplicates = bases.count(base) > 1

            if has_duplicates:
                # Rimuovi SOLO le parentesi tonde vuote o con spazi
                prev = None
                while prev != s:
                    prev = s
                    s = re.sub(r'\(\s*\)', '', s)
            else:
                # Nessun duplicato: rimuovi tutte le parentesi tonde
                prev = None
                while prev != s:
                    prev = s
                    s = re.sub(r'\([^()]*\)', '', s)

            # Parentesi quadre sempre rimosse
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\[[^\[\]]*\]', '', s)

            s = s.replace('"', '').replace("'", '')
            s = re.sub(r' {2,}', ' ', s).strip()
            m["NAME"] = s

    for b in station.get("bitinfo", []):

        if b["BITNAME"] is not None:
            s = b["BITNAME"]
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\([^()]*\)', '', s)
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\[[^\[\]]*\]', '', s)
            s = s.replace('"', '').replace("'", '')
            s = re.sub(r' {2,}', ' ', s).strip()
            b["BITNAME"] = s

        if b["TEXTON"] is not None:
            s = b["TEXTON"]
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\([^()]*\)', '', s)
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\[[^\[\]]*\]', '', s)
            s = s.replace('"', '').replace("'", '')
            s = re.sub(r' {2,}', ' ', s).strip()
            b["TEXTON"] = s

        if b["TEXTOFF"] is not None:
            s = b["TEXTOFF"]
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\([^()]*\)', '', s)
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r'\[[^\[\]]*\]', '', s)
            s = s.replace('"', '').replace("'", '')
            s = re.sub(r' {2,}', ' ', s).strip()
            b["TEXTOFF"] = s

output_json = json.dumps(data, indent=2, ensure_ascii=False)