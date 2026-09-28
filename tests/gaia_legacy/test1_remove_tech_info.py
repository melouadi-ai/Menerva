import json
import re

# Simuliamo il segnaposto della piattaforma
testo_grezzo = r'''{edge}[12]''' 

def pulisci_e_carica_json(testo):
    import json
    import re
 
    testo = testo.strip()
    
    # Se il testo contiene l'intestazione STATION INFORMATIONS, la puliamo con la regex
    if "STATION INFORMATIONS" in testo:
        testo = re.sub(r'^\[STATION INFORMATIONS\s*|\]$', '', testo)
    
    # Ora facciamo il parsing in sicurezza
    return json.loads(testo)

try:
    data = pulisci_e_carica_json(testo_grezzo)
    print("Successo! Dati caricati correttamente.")
    print(data)
except json.JSONDecodeError as e:
    print(f"Errore di parsing. Il testo finale era: {repr(testo_grezzo)}")
    print(f"Dettaglio errore: {e}")