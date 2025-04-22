import asyncio
import os
import sys
import datetime
from datetime import datetime

from telethon import types
from telethon.tl import functions
from telethon.tl.functions.account import GetPrivacyRequest, SetPrivacyRequest
from telethon.tl.types import MessageService, MessageMediaPhoto, MessageMediaWebPage, MessageMediaDocument, PeerUser, \
    User, UserStatusOffline, ChannelParticipantsAdmins, ChannelFull, PhotoEmpty, PeerNotifySettings, ChatInviteExported, \
    ChatReactionsAll, Channel, ChatPhotoEmpty, ChatAdminRights, ChatBannedRights, Chat, InputChannel
from telethon.tl.types.messages import ChatFull

from utils.dbutils import DbUtil_user, DbUtil_group, DbUtil_channel, DbUtil_selfinfo, DbUtil_entityinfo, \
    DbUtil_groupparticipant
from utils.config import getconf
from utils.tgutil import TgScraper
from utils.user_info import UserInfo
from utils.utilstool import str_to_bool

user_chat = []
group_chat = []
channel_chat = []
dialog_info =[]
user_list = []
group_list = []
user_chat_history = []
class SeparateSession(TgScraper):
    def __init__(self, work_path=None, proxy=None):
        super().__init__(tdata_path=work_path, proxy=proxy)
        self.limit = None
        self.wait_time = None
        self.config_list = []
        self.save_path = ''
        self.file_size = 0
        self.edit_lastseen = False

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
            elif key == 'edit_lastseen':
                self.edit_lastseen = str_to_bool(value)
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
                #sender_name = f"{message.sender.last_name or ''}{'-' if user.last_name and user.first_name else ''}{message.sender.first_name or ''}"
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
            message_type, media_content = 0, ""
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
            return lists

    async def get_channel_historymessage(self, channel):
        lists = []
        message_type, media_content = 0, ""
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
                            "sender_id": message.sender_id,
                            "message_type":message_type,
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
                            "sender_id": message.sender_id,
                            "message_type": 1,
                            "media_content": "",
                            "text_content": message.text,
                            "message_id": message.id,
                        }
                        lists.append(message_dict)
            except:
                pass

        return lists

    async def get_session(self):
        try:
            await super().get_session()
            self.getconf()
            await self.client.connect()

            me = await self.client.get_me()

            user_chat,group_chat,channel_chat,dialog_info = await self.get_dialog_entiry()

            user_chat_history = await self.dispatch_center(user_chat, "user")
            group_chat_history = await self.dispatch_center(group_chat, "group")
            channel_chat_history = await self.dispatch_center(channel_chat, "channel")

            participant_list = await self.get_group_participant(group_chat)

            if self.edit_lastseen is True:
                await self.edit_lastseen_status()

            await self.client.disconnect()

            userinfo = UserInfo(0)
            db_user = DbUtil_user(self.save_path, userinfo.get_userid(), user_chat, user_chat_history)
            db_user.run()
            db_group = DbUtil_group(self.save_path, userinfo.get_userid(), group_chat, group_chat_history)
            db_group.run()
            db_channel = DbUtil_channel(self.save_path, userinfo.get_userid(), channel_chat, channel_chat_history)
            db_channel.run()
            DbUtil_selfinfo(self.save_path, me).run()
            DbUtil_entityinfo(self.save_path, me, dialog_info).run()
            DbUtil_groupparticipant(self.save_path, userinfo.get_userid(), participant_list).run()

            #print(f'当前用户记录保存完成，请在{self.save_path}下查看数据库{userinfo.get_userid()}.db')

        except Exception as e:
            await self.client.disconnect()
            #print(f"出现异常: {e} ,结束连接")
            raise e

    def run(self):
        try:
            asyncio.run(self.get_session())

        except Exception as e:
            print(f'获取当前用户聊天记录出错{e},检查异常信息')
            raise e
            pass






