"""
存储城市天气报警信息
"""
import json

import loggers
import lib
import config
from loggers import scheLog


def get_alarms():
    rlt = []
    public_info = {}
    alarm_data = lib.api.get("http://www.weather.com.cn/data/alarm_xml/alarminfo.xml", rlt_type="xml2dict")
    alarm_info = alarm_data.get("AlermInfo")
    
    for key, value in alarm_info.items():
        scheLog.debug(json.dumps({"key": key, "value": value}, ensure_ascii=False))
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
                    if 0 and k in ("lon", "lat"):
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
                data = {k:v for k, v in dict_alarm_info.items() if k in ('id', 'lon', 'lat', 'signalType', 'signalLevel', 'issueTime', 'relieveTime', 'issueContent', 'dt')}
                yield (city_id, data)

def is_alarm_new(data: dict, new_data: dict):
    if data["status"] == 404:
        return True
    o_alarm_data = data.get("alarm_infos")
    if o_alarm_data and isinstance(o_alarm_data, list):
        o_alarm_data = ';'.join([ i["issueContent"] for i in o_alarm_data ])
    else:
        o_alarm_data = str(o_alarm_data)
    n_alarm_data = new_data.get("issueContent")
    if not n_alarm_data:
        # TODO 没内容有些奇怪
        scheLog.error(f'is_alarm_new: "(❤ ω ❤)"')
        return False
    elif o_alarm_data == n_alarm_data:
        return False
    return True

def save_alarms() -> (bool, dict):
    """
    调用获取警报, 存入警报信息
    """
    num_save, num_wrong = 0, 0
    for city_id, data in get_alarms():
        url = f"{config.API_DB_SERVER_HOST}/citys/{city_id}/alarm_infos/"
        city_weather_alarm = lib.api.get(f"{config.API_DB_SERVER_HOST}/citys/{city_id}", rlt_type="json")
        
        if not is_alarm_new(city_weather_alarm, data):
            # 除重
            continue
        loggers.weatherLog.info(json.dumps(data, ensure_ascii=False))
        rlt = lib.api.post(url, json=data, rlt_type="json")
        if rlt:
            sign = True
        else:
            sign = False
        data["id"] = city_id
        yield sign, data

def weather_alarm():
    """
    获取新警报信息, 查询覆盖范围内的用户, 推送之
    """
    for sign, data in save_alarms():
        if not data.get("id"):
            # TODO 非城市通告信息, 也可能为城市补充信息
            scheLog.debug(json.dumps(data, ensure_ascii=False))
            continue
        try:
            city_id = data["id"]
            list_user_info = [''] * 100
            skip = 0
            while len(list_user_info) == 100:
                url = f"{config.API_DB_SERVER_HOST}/users/bycity/{city_id}?skip={skip}&limit=100"
                skip = 100
                list_user_info = lib.api.get(url, rlt_type="json")
                issueContent = data["issueContent"]
                for user_info in list_user_info:
                    openid = user_info["openid"]
                    scheLog.debug(f"weather_alarm will send: {user_id}, {issueContent}")
                    lib.user_interface.send_wx_text(openid, txt=issueContent)
        except:
            scheLog.error(json.dumps(data, ensure_ascii=False))

if "__main__" == __name__:
    print(save_alarms())
