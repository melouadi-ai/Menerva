import json

json_input = r''' {edge}[17] '''
'''       
        "MEASUREID": 1,
        "BITNO": 2,
        "BITNAME": "PM-302B IN MARCIA",
        "TEXTON": "",
        "TEXTOFF": ""
'''


json_input = json.loads(json_input)

for station in json_input:
    if station.get('bitinfo', ''):
        for bit in station.get('bitinfo'):
            if not (bit.get('TEXTON') and bit.get('TEXTOFF')):
                bit['TEXTON'] = 'ON'
                bit['TEXTOFF'] = 'OFF'

result = json.dumps(json_input, indent=4, ensure_ascii=False)

print(result)