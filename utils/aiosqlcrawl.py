import asyncio
import os
import sys
from datetime import datetime

from telethon import types
from telethon.tl import functions
from telethon.tl.types import MessageService, MessageMediaPhoto, MessageMediaWebPage, MessageMediaDocument

from utils.dbutils import DbUtil_user, DbUtil_group, DbUtil_channel, DbUtil_selfinfo, DbUtil_entityinfo, \
    DbUtil_groupparticipant
from utils.aiodb import ChannelHandler, GroupHandler
from utils.config import getconf
from utils.tgutil import TgScraper
from utils.utilstool import _get_last, clear_curr
from utils.user_info import UserInfo

user_chat = []
group_chat = []
channel_chat = []
dialog_info =[]
user_list = []
group_list = []
user_chat_history = []
class AiodbSession(TgScraper):
    def __init__(self, work_path=None, proxy=None):
        super().__init__(tdata_path=work_path, proxy=proxy)
        self.limit = None
        self.wait_time = None
        self.save_path = ''
        self.file_size = 0

    def getconf(self):
        conf_dict = getconf('config.ini')
        for key, value in conf_dict.items():
            if key == 'limit':
                if value.lower() == 'none':
                    continue
                else:
                    self.limit = int(value)
                    continue
            elif key == 'wait_time':
                if value.lower() == 'none':
                    continue
                else:
                    self.wait_time = int(value)
                    continue
            elif key == 'save_path':
                if value.lower() == 'none':
                    continue
                else:
                    self.save_path = str(value)
                    continue
            elif key == 'max_size':
                if value.lower() == 'none':
                    continue
                else:
                    self.file_size = int(value)
                    continue

    async def edit_lastseen_status(self):
        await self.client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyStatusTimestamp(),
            rules=[types.InputPrivacyValueAllowAll()]
        ))

    async def get_chat_historymessage(self, user):
        lists = []
        message_type, media_content = 1, ""
        async for message in self.client.iter_messages(user, wait_time=self.wait_time):
            try:
                if type(message) == MessageService:
                    continue
                # sender_name = f"{message.sender.last_name or ''}{'-' if user.last_name and user.first_name else ''}{message.sender.first_name or ''}"
                dt = message.date.strftime('%Y-%m-%d %H:%M:%S')
                if message.media:
                    if message.file:
                        if isinstance(message.media, MessageMediaPhoto):
                            message_type = 3
                            media_content = message.file.name
                        elif isinstance(message.media, MessageMediaWebPage):
                            message_type = 2
                            media_content = message.media.webpage.url
                        elif isinstance(message.media, MessageMediaDocument):
                            message_type = 4
                            media_content = message.file.name
                    message_dict = {
                        "time": dt,
                        "sender_id": message.sender_id,
                        "message_type": message_type,
                        "media_content": media_content,
                        "text_content": message.text,
                        "message_id": message.id
                    }
                    if message.file.size < self.file_size:
                        await message.download_media(self.save_path)
                    lists.append(message_dict)
                else:
                    message_dict = {
                        "time": dt,
                        "sender_id": message.sender_id,
                        "message_type": 1,
                        "media_content": "",
                        "text_content": message.text,
                        "message_id": message.id
                    }
                    lists.append(message_dict)
            except:
                pass
        return lists


    async def get_group_historymessage(self, group):
            lists = []
            message_type, media_content = 1, ""

            async for message in self.client.iter_messages(group, limit=self.limit, wait_time=self.wait_time):
                try:
                    if type(message) == MessageService:
                        continue
                    else:
                        if message.file:
                            if isinstance(message.media, MessageMediaPhoto):
                                message_type = 3
                                media_content = message.file.name
                            elif isinstance(message.media, MessageMediaWebPage):
                                message_type = 2
                                media_content = message.media.webpage.url
                            elif isinstance(message.media, MessageMediaDocument):
                                message_type = 4
                                media_content = message.file.name
                            message_dict = {
                                "time": message.date.strftime('%Y-%m-%d %H:%M:%S'),
                                "group_id": group.id,
                                "sender_id": message.sender_id,
                                "message_type": message_type,
                                "media_content": media_content,
                                "text_content": message.text,
                                "message_id": message.id,
                                "reply_to": message.reply_to
                            }
                            lists.append(message_dict)
                            if message.file.size < self.file_size:
                                await message.download_media(self.save_path)

                        else:
                            message_dict = {
                                "time": message.date.strftime('%Y-%m-%d %H:%M:%S'),
                                "group_id": group.id,
                                "sender_id": message.sender_id,
                                "message_type": 1,
                                "media_content": "",
                                "text_content": message.text,
                                "message_id": message.id,
                                "reply_to": message.reply_to
                            }
                            lists.append(message_dict)
                except:
                    pass
            try:
                await GroupHandler(self.save_path, UserInfo(0).get_userid(), lists).handle_io()
                return []
            except:
                return []


    async def get_channel_historymessage(self, channel):
        lists = []
        message_type, media_content = 1, ""
        async for message in self.client.iter_messages(channel, limit=self.limit, wait_time=self.wait_time):
            try:
                if type(message) == MessageService:
                    continue
                else:
                    if message.file:
                        if isinstance(message.media, MessageMediaPhoto):
                            message_type = 3
                            media_content = message.file.name
                        elif isinstance(message.media, MessageMediaWebPage):
                            message_type = 2
                            media_content = message.media.webpage.url
                        elif isinstance(message.media, MessageMediaDocument):
                            message_type = 4
                            media_content = message.file.name
                        message_dict = {
                            "time": message.date.strftime('%Y-%m-%d %H:%M:%S'),
                            "channel_id": channel.id,
                            "sender_id": message.sender_id,
                            "message_type": message_type,
                            "media_content": media_content,
                            "text_content": message.text,
                            "message_id": message.id,
                        }
                        lists.append(message_dict)
                        if message.file.size < self.file_size:
                            await message.download_media(self.save_path)

                    else:
                        message_dict = {
                            "time": message.date.strftime('%Y-%m-%d %H:%M:%S'),
                            "channel_id": channel.id,
                            "sender_id": message.sender_id,
                            "message_type": 1,
                            "media_content": "",
                            "text_content": message.text,
                            "message_id": message.id,
                        }
                        lists.append(message_dict)
            except:
                pass
        try:
            await ChannelHandler(self.save_path, UserInfo(0).get_userid(), lists).handle_io()
            return []
        except:
            return []

    async def get_session(self):
        try:
            await super().get_session()
            self.getconf()
            await self.client.connect()

            me = await self.client.get_me()
            userinfo = UserInfo(0)
            user_chat,group_chat,channel_chat,dialog_info = await self.get_dialog_entiry()
            user_chat_history = await self.dispatch_center(user_chat, "user")
            DbUtil_user(self.save_path, userinfo.get_userid(), user_chat, user_chat_history).run()
            DbUtil_selfinfo(self.save_path, me).run()
            DbUtil_entityinfo(self.save_path, me, dialog_info).run()

            participant_list = await self.get_group_participant(group_chat)
            DbUtil_groupparticipant(self.save_path, me.id, participant_list).run()


            await self.dispatch_center(group_chat, "group")
            await self.dispatch_center(channel_chat, "channel")

            await self.client.disconnect()

        except:
            await self.client.disconnect()

    def run(self):
        try:
            asyncio.run(self.get_session())
            print('当前用户记录保存完成，请在配置文件中指定的路径{}下查看数据库'.format(self.save_path))
        except:
            pass






