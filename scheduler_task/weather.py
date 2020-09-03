from . import lib

def get_alarms():
    rlt = []
    for i in rlt:
        yield i

def save_alarms() -> (int, int):
    num_save, num_wrong = 0, 0
    for alarm in get_alarms():
        sign = save2db("weather_alarm", alarm)
        if not sign:
            num_wrong += 1
        else:
            num_save += 1
    return num_save, num_wrong    
