import json

input_json = r'''{edge}[13]'''

try:
    input_json = json.loads(input_json)

    for station in input_json:
        station['bitinfo'] = []

    result = json.dumps(input_json, indent=4, ensure_ascii=False)

    print('Success')
	
except Exception as e:
    print(f'Error: {e}')