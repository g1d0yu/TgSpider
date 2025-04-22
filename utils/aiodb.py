import asyncio
import os

import aiosqlite
from abc import ABC, abstractmethod

lock = asyncio.Lock()
class DbHandler(ABC):
    def __init__(self, save_path=None, userid=None, data_list=None):
        self.db_path = os.path.join(save_path, str(userid) + '.db')
        self.data_list = data_list
        asyncio.create_task(self.init_db())

    @abstractmethod
    async def init_db(self):
        pass

    async def execute_db_query(self, query, data):
        async with lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.executemany(query, data)
                await db.commit()

class ChannelHandler(DbHandler):
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'CREATE TABLE IF NOT EXISTS channel_broast (id INTEGER PRIMARY KEY, time TEXT,channel_id TEXT, sender_id TEXT,message_type TEXT,media_content TEXT, text_content TEXT,message_id TEXT)')
            await db.commit()

    async def handle_io(self):
        insert_query = f"INSERT INTO channel_broast (time,channel_id,sender_id, message_type, media_content, text_content, message_id) VALUES (:time, :channel_id,  :sender_id, :message_type, :media_content, :text_content, :message_id)"
        await self.execute_db_query(insert_query, self.data_list)

class GroupHandler(DbHandler):
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'CREATE TABLE IF NOT EXISTS group_chat (id INTEGER PRIMARY KEY, time TEXT,group_id TEXT,sender_id TEXT,message_type TEXT,media_content TEXT, text_content TEXT,message_id TEXT,reply_to TEXT)')
            await db.commit()

    async def handle_io(self):
        insert_query = f"INSERT INTO group_chat (time,group_id,sender_id,message_type, media_content, text_content, message_id, reply_to) VALUES (:time, :group_id, :sender_id,:message_type, :media_content, :text_content, :message_id, :reply_to)"
        await self.execute_db_query(insert_query, self.data_list)