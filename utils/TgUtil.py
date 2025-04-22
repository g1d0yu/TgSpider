import asyncio
from abc import ABC, abstractmethod
from opentele.td import TDesktop
from opentele.api import API, UseCurrentSession
from telethon.tl.functions.channels import GetFullChannelRequest
#from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import MessageService, ChannelParticipantsAdmins

from utils.user_info import UserInfo


class TgScraper(ABC):

    def __init__(self, tdata_path, proxy=None):
        self.tdata_path = tdata_path
        self.proxy = proxy
        self.client = None
        self._tdesk = None

    @abstractmethod
    async def get_chat_historymessage(self,user):
        pass

    @abstractmethod
    async def get_group_historymessage(self, group):
        pass

    @abstractmethod
    async def get_channel_historymessage(self, channel):
        pass

    async def dispatch_center(self, list, task_type):
        if task_type == "user":
            tasks = [self.get_chat_historymessage(item) for item in list]
            results = await asyncio.gather(*tasks)
        elif task_type == "group":
            tasks = [self.get_group_historymessage(item) for item in list]
            results = await asyncio.gather(*tasks)
        else:
            tasks = [self.get_channel_historymessage(item) for item in list]
            results = await asyncio.gather(*tasks)
        return results

    async def get_dialog_entiry(self):
        user_chat = []
        group_chat = []
        channel_chat = []
        dialog_info = []
        async for dialog in self.client.iter_dialogs():
            if dialog.is_user == True:
                user_chat.append(dialog.entity)
                dialog_info.append(dialog.entity)
                continue
            if dialog.is_group == True:
                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                    try:
                        ch_full = await self.client(GetFullChannelRequest(dialog.entity))
                        dialog_info.append(ch_full)
                    except:
                        dialog_info.append(dialog.entity)
                else:
                    try:
                        group_chat.append(dialog.entity)
                        ch_full = await self.client(GetFullChannelRequest(dialog.entity))
                        dialog_info.append(ch_full)
                    except:
                        pass
                continue
            elif dialog.is_channel == True:
                if hasattr(dialog.entity, 'username') and dialog.entity.username:
                    pass
                else:
                    channel_chat.append(dialog.entity)
                dialog_info.append(dialog.entity)
                continue

        return user_chat, group_chat, channel_chat, dialog_info

    async def get_group_participant(self, group_chat):
        participant_list = []

        for item in group_chat:
            user_list = []
            admin_id_set = set()
            try:
                async for user in self.client.iter_participants(item):
                    participant_dict = {
                        "group_id": item.id,
                        "user_id": user.id,
                        "name": f"{user.last_name or ''}{'-' if user.last_name and user.first_name else ''}{user.first_name or ''}",
                        "username": f"{user.username or ''}",
                        "is_admin": 0

                    }
                    user_list.append(participant_dict)

                async for admin in self.client.iter_participants(item, filter=ChannelParticipantsAdmins):
                    admin_id_set.add(admin.id)

                for user in user_list:
                    if user['user_id'] in admin_id_set:
                        user['is_admin'] = 1
            except:
                pass
            participant_list.append(user_list)

        return participant_list

    async def get_session(self):

        self._tdesk = TDesktop(self.tdata_path)
        UserInfo(self._tdesk.accounts[0].UserId)
        try:
            newAPI = API.TelegramDesktop.Generate()
            self.client = await self._tdesk.ToTelethon(session=None, flag=UseCurrentSession, api=newAPI, proxy=self.proxy)
        except:
            print('出现未知种类的错误，请尝试更新库')
            pass


