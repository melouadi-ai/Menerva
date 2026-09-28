import json

# ==========================================
# ESEMPIO DI UTILIZZO
# ==========================================
# La tua stringa di input
input_string = r'''{edge}[8]'''

try:
    # 1. PULIZIA DELLA STRINGA (da fare PRIMA del parsing)
    clean_string = input_string.replace("```json", "").replace("```", "").strip()

    # 2. Parsing della stringa JSON pulita in un oggetto Python
    data = json.loads(clean_string)

    # 3. Iterazione e ordinamento
    for device in data:
        if "measures" in device:
            # Ordina in 3 gruppi: 
            # 0 = Numeri (vanno in cima, ordinati numericamente)
            # 1 = Stringhe (vanno in fondo, ordinate alfabeticamente)
            # 2 = Null / Nessun valore (vanno alla fine assoluta)
            device["measures"].sort(
                key=lambda x: (
                    0, x.get("MODBUSREGISTRO")
                ) if isinstance(x.get("MODBUSREGISTRO"), (int, float)) else (
                    1, x.get("MODBUSREGISTRO")
                ) if isinstance(x.get("MODBUSREGISTRO"), str) else (
                    2, ""
                )
            )
        
        if "bitinfo" in device:
            # Stessa logica per MEASUREID
            device["bitinfo"].sort(
                key=lambda x: (
                    0, x.get("MEASUREID")
                ) if isinstance(x.get("MEASUREID"), (int, float)) else (
                    1, x.get("MEASUREID")
                ) if isinstance(x.get("MEASUREID"), str) else (
                    2, ""
                )
            )

    # 4. Conversione dell'oggetto Python di nuovo in stringa JSON
    output_string = json.dumps(data, indent=2, ensure_ascii=False)
    print(output_string)

except json.JSONDecodeError as e:
    # Gestione dell'errore
    output_string = json.dumps({'Errore': 'Stringa input invalida'})
    print(output_string)