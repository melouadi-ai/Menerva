import json

# ==========================================
# ESEMPIO DI UTILIZZO
# ==========================================
# La tua stringa di input
input_string = r'''{edge}[17]'''

try:
    # 1. PULIZIA DELLA STRINGA (da fare PRIMA del parsing)
    clean_string = input_string.replace("```json", "").replace("```", "").strip()

    # 2. Parsing della stringa JSON pulita in un oggetto Python
    data = json.loads(clean_string)

    # 3. Iterazione e ordinamento
    for device in data:
        if "measures" in device:
            # Ordina in base a MODBUSREGISTRO. Se nullo o non numerico, finisce in fondo.
            device["measures"].sort(
                key=lambda x: (0, int(x.get("MODBUSREGISTRO"))) 
                if x.get("MODBUSREGISTRO") is not None and str(x.get("MODBUSREGISTRO")).lstrip('-').isdigit() 
                else (1, 0)
            )
        
        if "bitinfo" in device:
            # Ordina in base a MEASUREID. Se nullo o non numerico, finisce in fondo.
            device["bitinfo"].sort(
                key=lambda x: (0, int(x.get("MEASUREID"))) 
                if x.get("MEASUREID") is not None and str(x.get("MEASUREID")).lstrip('-').isdigit() 
                else (1, 0)
            )

    # 4. Conversione dell'oggetto Python di nuovo in stringa JSON
    output_string = json.dumps(data, indent=2, ensure_ascii=False)
    print(output_string)

except json.JSONDecodeError as e:
    # Corretto l'errore di sintassi aggiungendo le parentesi graffe per formare un dizionario
    output_string = json.dumps({'Errore': 'Stringa input invalida'})
    print(output_string)