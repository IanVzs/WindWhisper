from . import lib


"""
'dt', 'hourType', 'RoadIcing', 'SnowStorm', 'RainStorm', 'Hail', 'Gale', 'HeavyFog', 'HeatWave', 'Drought', 'ColdWave', 'SW_Hazards', 'Lightning', 'Haze', 'SandStorm', 'Frost', 'Typhoon', 'other'

city1: 
city2:
.
.
.
cityn:
"""

def get_alarms():
    rlt = []
    public_info = {}
    alarm_data = lib.api.get("http://www.weather.com.cn/data/alarm_xml/alarminfo.xml", rlt_type="xml2dict")
    alarm_info = alarm_data.get("AlermInfo")
    
    for key, value in alarm_info.items():
        if isinstance(value, str) and (key.replace('@', '') not in public_info or value != public_info[key]):
            public_info[key.replace('@', '')] = value
        elif value == None:
            continue
        elif isinstance(value, dict):
            stations_info = value.get("Station")
            stations_info = stations_info if isinstance(stations_info, list) else [stations_info]
            for _s_info in stations_info:
                _s_info.update(public_info)
                dict_alarm_info = {}
                _s_info = {k.replace('@', ''):v for k, v in _s_info.items()}
                for k, v in _s_info.items():
                    k = k.replace('@', '')
                    if k in ("stationId", "hourType"):
                        continue
                    if k in ("lon", "lat"):
                        from decimal import Decimal
                        if v:
                            v = Decimal(v)
                        else:
                            v = Decimal(0)
                    elif k in ("issueTime", "relieveTime", "dt"):
                        from datetime import datetime
                        if len(v) == len("20200908115400"):
                            v = datetime.strptime(v, "%Y%m%d%H%M%S")
                            v = v.strftime("%Y-%m-%d %H:%M:%S")
                        elif len(v) == len("20200908"):
                            v = datetime.strptime(v, "%Y%m%d")
                            v = v.strftime("%Y-%m-%d")
                        else:
                            v = ''
                    dict_alarm_info[k] = v
                city_id = dict_alarm_info["areaId"]
                if len(city_id) == len("1010609"):
                    # 市
                    city_id += "00"
                elif len(city_id) == len("101281801"):
                    # 县
                    pass
                elif len(city_id) == len("10106"):
                    # 省
                    city_id += "0000"
                stationName = dict_alarm_info["stationName"]
                # TODO 如果`city`中无, 则新增该地点
                url = "http://127.0.0.1:4545/citys/{city_id}/alarm_infos/"
                data = {k:v for k, v in dict_alarm_info.items() if k in ('id', 'lon', 'lat', 'signalType', 'signalLevel', 'issueTime', 'relieveTime', 'issueContent', 'dt')}
                yield (url, data)

def save_alarms() -> (int, int):
    num_save, num_wrong = 0, 0
    for url, data in get_alarms():
        lib.api.post()
        if not sign:
            num_wrong += 1
        else:
            num_save += 1
    return num_save, num_wrong    
