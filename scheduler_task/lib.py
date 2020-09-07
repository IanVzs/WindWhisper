import sqlite3

class Data:
    def __init__(self):
        _sqlite3()

    def _sqlite3(self, data):
        self.sqlite3_conn = sqlite3.connect('../city_info.db')
        self.sqlite3_cursor = sqlite3_conn.cursor()
        
    def save_data(self, db_name, table_name, data: dict):
        list_keys = []
        str_keys = ''
        list_values = ''
        str_values = ''
        for key, value in data.items():
            list_keys.append(key)
            if isinstance(value, str):
                value  = f"'{value}'"
            list_values.append(str(value))
        str_keys = ','.join(list_keys)
        str_values ','.join(list_values)
        self.sqlite3_cursor.execute(f"INSERT INTO {table_name} ({str_keys}) \
      VALUES ({str_values})")
    def save_done(self):
        self.sqlite3_conn.commit()
        self.sqlite3_conn.close()

    def get_data(self):
        pass
    
def init_city_info():
    """先存好城市信息"""
    engi_data = Data()
    for line in lines:
        pass
        item_data = {
            "db_name": "",
            "table_name": "",
            "data": {
                "id": ''
                "lon": ''
                "lat": ''
                "cityZh": ''
                "provinceZh": ''
                "leaderZh": ''
            }
        }
        engi_data.save_data(**item_data)
    engi_data.save_done()

if "__main__" == __name__:
    init_city_info()
    