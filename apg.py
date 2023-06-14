import asyncpg
import asyncio
from config import DB



class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    async def close(self):
        await self.pool.close()



    async def execute(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as connection:
            result = await connection.execute(query, *args)
        await self.close()
        return result
        

    async def fetch(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as connection:
            result = await connection.fetch(query, *args)
        await self.close()
        return result

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return result

    async def fetchval(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as connection:
            result = await connection.fetchval(query, *args)
        await self.close()
        return result

    async def selectd(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as connection:
            result = await connection.fetch(query, *args)
            columns = result[0].keys()
            res =  [dict(row) for row in result]
        await self.close()
        return res


async def main():
    db = Database(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
    

    result = await db.selectd("SELECT id, order_status FROM order_info WHERE order_status = 'posted';")
    for row in result:
        print(row)




loop = asyncio.get_event_loop()
loop.run_until_complete(main())