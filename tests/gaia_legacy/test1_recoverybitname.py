import json

json_input = r''' [
  {
    "NAME": "SME",
    "DRIVERNAME": "modbusplc",
    "XPOSITION": 430,
    "YPOSITION": 530,
    "DOWNLOADTYPE": 0,
    "DOWNLOADPROGRAM": null,
    "IGNOREERRORS": 0,
    "SNAPSHOT": null,
    "NORMALSNAPSHOT": 1,
    "CRITICSNAPSHOT": 32767,
    "ALARMSNAPSHOT": 32767,
    "SYNOBITMAP": null,
    "LINENAME": null,
    "AREACODE": null,
    "ADDRESS": null,
    "LINECONFIGURATION": null,
    "TIMELASTCONFIGURATION": null,
    "TIMELASTDOWNLOAD": null,
    "EVENTTIME": null,
    "EVENTCODE": 0,
    "EVENTORIGIN": null,
    "CODE": null,
    "DRIVERPRIVATE": null,
    "OVERWRITEMEASURES": 1,
    "DRIVERCONFIG": "<configuration><commProto><p0 class=\"Protocollo MODBUS (master) via TCP/IP\" name=\"Protocollo MODBUS (master) via TCP/IP\" ipaddress=\"10.100.50.95\" tcpport=\"511\" timeout=\"5000\" retries=\"3\" write4XXXX=\"6\"/></commProto><recoveryProto/></configuration>",
    "ID": 1,
    "measures": [
      {
        "STATIONID": 1,
        "NAME": "Ingressi digitali 1",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": null,
        "HIGHCRITICAL": null,
        "LOWRANGE": null,
        "HIGHRANGE": null,
        "LOWOFFSET": null,
        "HIGHOFFSET": null,
        "SQRAW": null,
        "SQ1HOURMEAN": null,
        "SQ3HOURMEAN": null,
        "SQ8HOURMEAN": null,
        "SQDAILYMEAN": null,
        "UNITS": null,
        "STANDARDRANGEID": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "DRIVERPRIVATE": "0x050000000000000000000000000000000100000096000000",
        "ONLY_POSITIVES": null,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 1,
        "UNITS2": null
      },
      {
        "STATIONID": 1,
        "NAME": "Ingressi digitali 2",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": null,
        "HIGHCRITICAL": null,
        "LOWRANGE": null,
        "HIGHRANGE": null,
        "LOWOFFSET": null,
        "HIGHOFFSET": null,
        "SQRAW": null,
        "SQ1HOURMEAN": null,
        "SQ3HOURMEAN": null,
        "SQ8HOURMEAN": null,
        "SQDAILYMEAN": null,
        "UNITS": null,
        "STANDARDRANGEID": null,
        "DRIVERDATA": 2,
        "TYPE": 1,
        "DRIVERPRIVATE": "0x060000000000000000000000000000000100000096000000",
        "ONLY_POSITIVES": null,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 2,
        "UNITS2": null
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola N2",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": -3.40282e+38,
        "HIGHCRITICAL": 3.40282e+38,
        "LOWRANGE": -3.40282e+38,
        "HIGHRANGE": 3.40282e+38,
        "LOWOFFSET": -3.40282e+38,
        "HIGHOFFSET": 3.40282e+38,
        "SQRAW": 3.40282e+38,
        "SQ1HOURMEAN": 3.40282e+38,
        "SQ3HOURMEAN": 3.40282e+38,
        "SQ8HOURMEAN": 3.40282e+38,
        "SQDAILYMEAN": 3.40282e+38,
        "UNITS": null,
        "STANDARDRANGEID": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "DRIVERPRIVATE": "0x0900000000000000000000000000000001000000FA000000",
        "ONLY_POSITIVES": 0,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 3,
        "UNITS2": null
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola ARI",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": -3.40282e+38,
        "HIGHCRITICAL": 3.40282e+38,
        "LOWRANGE": -3.40282e+38,
        "HIGHRANGE": 3.40282e+38,
        "LOWOFFSET": -3.40282e+38,
        "HIGHOFFSET": 3.40282e+38,
        "SQRAW": 3.40282e+38,
        "SQ1HOURMEAN": 3.40282e+38,
        "SQ3HOURMEAN": 3.40282e+38,
        "SQ8HOURMEAN": 3.40282e+38,
        "SQDAILYMEAN": 3.40282e+38,
        "UNITS": null,
        "STANDARDRANGEID": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "DRIVERPRIVATE": "0x0A00000000000000000000000000000001000000FA000000",
        "ONLY_POSITIVES": 0,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 4,
        "UNITS2": null
      },
      {
        "STATIONID": 1,
        "NAME": "QAL3: Tempo trascorso apertura elettrovalvola SO2",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": -3.40282e+38,
        "HIGHCRITICAL": 3.40282e+38,
        "LOWRANGE": -3.40282e+38,
        "HIGHRANGE": 3.40282e+38,
        "LOWOFFSET": -3.40282e+38,
        "HIGHOFFSET": 3.40282e+38,
        "SQRAW": 3.40282e+38,
        "SQ1HOURMEAN": 3.40282e+38,
        "SQ3HOURMEAN": 3.40282e+38,
        "SQ8HOURMEAN": 3.40282e+38,
        "SQDAILYMEAN": 3.40282e+38,
        "UNITS": null,
        "STANDARDRANGEID": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "DRIVERPRIVATE": "0x0B00000000000000000000000000000001000000FA000000",
        "ONLY_POSITIVES": 0,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 5,
        "UNITS2": null
      },
      {
        "STATIONID": 1,
        "NAME": "SO2 Raw",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": -3.40282e+38,
        "HIGHCRITICAL": 3.40282e+38,
        "LOWRANGE": -3.40282e+38,
        "HIGHRANGE": 3.40282e+38,
        "LOWOFFSET": -3.40282e+38,
        "HIGHOFFSET": 3.40282e+38,
        "SQRAW": 3.40282e+38,
        "SQ1HOURMEAN": 3.40282e+38,
        "SQ3HOURMEAN": 3.40282e+38,
        "SQ8HOURMEAN": 3.40282e+38,
        "SQDAILYMEAN": 3.40282e+38,
        "UNITS": "mg/Nm3",
        "STANDARDRANGEID": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "DRIVERPRIVATE": "0x1100000000000000000000000000000001000000FA000000",
        "ONLY_POSITIVES": 0,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 6,
        "UNITS2": "mg/Nm3"
      },
      {
        "STATIONID": 1,
        "NAME": "Temperatura fumi Raw",
        "DISABLED": 0,
        "DIGITAL": null,
        "DOWNLOAD": 0,
        "SNAPSHOT": 1,
        "IGNOREERRORS": 0,
        "LOWCRITICAL": -3.40282e+38,
        "HIGHCRITICAL": 3.40282e+38,
        "LOWRANGE": -3.40282e+38,
        "HIGHRANGE": 3.40282e+38,
        "LOWOFFSET": -3.40282e+38,
        "HIGHOFFSET": 3.40282e+38,
        "SQRAW": 3.40282e+38,
        "SQ1HOURMEAN": 3.40282e+38,
        "SQ3HOURMEAN": 3.40282e+38,
        "SQ8HOURMEAN": 3.40282e+38,
        "SQDAILYMEAN": 3.40282e+38,
        "UNITS": "°C",
        "STANDARDRANGEID": null,
        "DRIVERDATA": 0,
        "TYPE": 0,
        "DRIVERPRIVATE": "0x2100000000000000000000000000000001000000FA000000",
        "ONLY_POSITIVES": 0,
        "VM_SOURCE_CODE": "if elapsed() then    storep(11);else store(8);fi;",
        "PERIOD": 5,
        "SNAPSIZE": 1000,
        "DRIVERCONFIG": "<configuration SynopticAnalogicFormat=\\\"%7.2f\\\"/>",
        "ID": 7,
        "UNITS2": "°C"
      }
    ],
    "bitinfo": [
      {
        "MEASUREID": 1,
        "BITNO": 8,
        "BITNAME": "BLOCCO DA BSS2",
        "TEXTON": "BLOCCO",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 9,
        "BITNAME": "ALLARME BASSA PORTATA FT-2611",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 10,
        "BITNAME": "ALLARME BASSA PORTATA FT-310",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 11,
        "BITNAME": "ALLARME BASSA PORTATA FT-313",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 12,
        "BITNAME": "AI303A ALLARME BASSO PH",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 13,
        "BITNAME": "AI303B ALLARME BASSO PH",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 14,
        "BITNAME": "AI2602A ALLARME BASSO PH",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 15,
        "BITNAME": "AI2602B ALLARME BASSO PH",
        "TEXTON": "ALLARME",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 1,
        "BITNO": 1,
        "BITNAME": "PM-302A IN MARCIA",
        "TEXTON": "",
        "TEXTOFF": ""
      },
      {
        "MEASUREID": 1,
        "BITNO": 2,
        "BITNAME": "PM-302B IN MARCIA",
        "TEXTON": "",
        "TEXTOFF": ""
      },
      {
        "MEASUREID": 1,
        "BITNO": 4,
        "BITNAME": "PM-310A IN MARCIA",
        "TEXTON": "",
        "TEXTOFF": ""
      },
      {
        "MEASUREID": 1,
        "BITNO": 5,
        "BITNAME": "PM-310B IN MARCIA",
        "TEXTON": "",
        "TEXTOFF": ""
      },
      {
        "MEASUREID": 2,
        "BITNO": 8,
        "BITNAME": "PM-2600A IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 9,
        "BITNAME": "PM-2600B IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 10,
        "BITNAME": "PM-2601A IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 11,
        "BITNAME": "PM-2601B IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 12,
        "BITNAME": "PM-2604A IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 13,
        "BITNAME": "PM-2604B IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 0,
        "BITNAME": "VENTILATORE VN-400 IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 1,
        "BITNAME": "VENTILATORE VN-2504 IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 2,
        "BITNAME": "VENTILATORE 514K1 IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      },
      {
        "MEASUREID": 2,
        "BITNO": 3,
        "BITNAME": "VENTILATORE 514K2 IN MARCIA",
        "TEXTON": "MARCIA",
        "TEXTOFF": "OFF"
      }
    ]
  }
] '''

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