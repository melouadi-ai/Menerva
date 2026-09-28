import json

# Your input variables
input_station_info = r'''{edge}[12]'''
input_tech_data = r'''{edge}[11]'''
input_density_map = r'''{edge}[23]'''

# 1. Check if the string is empty (or just whitespace) before parsing
if input_station_info.strip():
    parsed_station_info = json.loads(input_station_info)
else:
    parsed_station_info = None

if input_tech_data.strip():
    parsed_tech_data = json.loads(input_tech_data)
else:
    parsed_tech_data = None

# 2. Proceed with your original logic using the parsed variables
if parsed_station_info and parsed_tech_data:
    # 1. Aggiungi l'elemento alla prima lista
    parsed_station_info.append(parsed_tech_data[0])
    
    # 2. Ora assegna la lista aggiornata a 'final'
    final = parsed_station_info
    
    result = json.dumps(final, indent=4, ensure_ascii=False)
    
elif parsed_station_info:
    result = json.dumps(parsed_station_info, indent=4, ensure_ascii=False)
    
elif parsed_tech_data:
    result = json.dumps(parsed_tech_data, indent=4, ensure_ascii=False)
    
else:
    result = ''

