import asyncio
import aiohttp
import sqlite3

from scheduler_task import config

class User_Interface:
    def __init__(self):
        pass
    
    def switch_way(self, user_info):
        email = user_info["email"]
        openid = user_info.get("wx_infos") and user_info["wx_infos"]["openid"]
        return "wx", openid

    def send_text(self, user_id: int, txt: str):
        user_info = lib.api.get("{config.API_DB_SERVER_HOST}/users/{user_id}", rlt_type="json")
        way, _id = switch_way(user_info)
        if "wx" == way:
            data = {"txt": txt, "openid": _id}
            print("已经发生...")
            user_info = lib.api.post("{config.API_DB_SERVER_HOST}/wx_api/send_txt", json=data, rlt_type="json")
        else:
            pass
        return 1


class API:
    def __init__(self):
        pass

    async def fetch(self, session, url, method="GET", data='', json:dict={}, rlt_type="read"):
        """
        data: byte or str
        """
        def req(session, url, method="GET", data='', json:dict={}):
            hi = ''
            if "GET" == method:
                hi = session.get(url)
            elif "POST" == method:
                if data:
                    hi = session.post(url, data=data)
                elif json:
                    hi = session.post(url, json=json)
            return hi

        async with req(session, url, method, data, json) as response:
            if rlt_type in ("read", "xml2dict"):
                rlt = await response.read()
                if rlt_type == "xml2dict":
                    import xmltodict
                    rlt = xmltodict.parse(rlt)
                return rlt
            elif rlt_type == "text":
                return await response.text()
            elif rlt_type == "json":
                return await response.json()

    def get(self, url, rlt_type="read"):
        async def _get(url, rlt_type):
            async with aiohttp.ClientSession() as session:
                a = await self.fetch(session, url, rlt_type=rlt_type)
            return a
        
        rlt = asyncio.run(_get(url, rlt_type=rlt_type))
        return rlt

    def post(self, url, data={}, json={}, rlt_type=''):
        async def _post(url, data={}, json={}):
            async with aiohttp.ClientSession() as session:
                a = await self.fetch(session, url, method="POST", data=data, json=json)
            return a
        rlt = asyncio.run(_post(url, data=data, json=json))
        return rlt


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
        str_values = ','.join(list_values)
        self.sqlite3_cursor.execute(f"INSERT INTO {table_name} ({str_keys}) \
      VALUES ({str_values})")
    def save_done(self):
        self.sqlite3_conn.commit()
        self.sqlite3_conn.close()

    def get_data(self):
        pass

#-----------------------------实例-----------------------------#
api = API()
user_interface = User_Interface()

if "__main__" == __name__:
    init_city_info()
    
