import asyncio
import aiohttp
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
        str_values = ','.join(list_values)
        self.sqlite3_cursor.execute(f"INSERT INTO {table_name} ({str_keys}) \
      VALUES ({str_values})")
    def save_done(self):
        self.sqlite3_conn.commit()
        self.sqlite3_conn.close()

    def get_data(self):
        pass

class API:
    def __init__(self):
        pass

    async def fetch(self, session, url, rlt_type="read"):
        async with session.get(url) as response:
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
                a = await self.fetch(session, url, rlt_type)
            return a
        
        rlt = asyncio.run(_get(url, rlt_type))
        return rlt

    def post(self, url, data={}, json={}):
        async def _post(url, data={}, json={}):
            async with aiohttp.ClientSession() as session:
                a = await self.fetch(session, 'https://www.baidu.com')
            return a
        rlt = asyncio.run(_post(url, data={}, json={}))
        return rlt

api = API()

if "__main__" == __name__:
    init_city_info()
    