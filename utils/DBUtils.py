import datetime
import json
import os
import sqlite3

from telethon import types
from telethon.tl.types import User, UserStatusOffline, UserStatusRecently


class DbUtil_util:
    def __init__(self, save_path=None, userid=None, entity_list=None, data_list=None):
        self.save_path= save_path
        self.userid = userid
        self.entity_list = entity_list
        self.data_list = data_list

    def create_table(self,cursor):
        raise NotImplementedError("Subclass must implement the 'create_table' method")

    def insert_data(self,cursor, entity_list, data_list):
        raise NotImplementedError("Subclass must implement the 'insert_data' method")

    def run(self):
        try:
            db_name = str(self.userid) + '.db'
            db_path = os.path.join(self.save_path, db_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            self.create_table(cursor)
            self.insert_data(cursor, self.entity_list, self.data_list)
            conn.commit()
            conn.close()
        except:
            pass


class DbUtil_user(DbUtil_util):

    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS private_chat (id INTEGER PRIMARY KEY, time TEXT NOT NULL, sender_id TEXT NOT NULL,receiver_id TEXT NOT NULL,message_type INT,media_content TEXT NOT NULL,text_content TEXT NOT NULL,message_id TEXT NOT NULL);"
        cursor.execute(create_table_sql)


    def insert_data(self,cursor, entity_list, data_list):
        try:
            for i in range(len(entity_list)):
                if len(data_list[i]) == 0:
                    continue
                else:
                    for j in range(len(data_list[i])):
                        time = data_list[i][j]['time']
                        sender_id = data_list[i][j]['sender_id']
                        #sender_name = data_list[i][j]['sender_name']
                        receiver_id = entity_list[i].id
                        #receiver_name = f"{entity_list[i].last_name or ''}{'-'}{entity_list[i].first_name or ''}"
                        message_type = data_list[i][j]['message_type']
                        media_content = f"{data_list[i][j]['media_content'] or ''}"
                        text_content = f"{data_list[i][j]['text_content'] or ''}"
                        message_id = data_list[i][j]['message_id']
                        insert_query = f"INSERT INTO private_chat (time, sender_id,receiver_id, message_type,media_content,text_content,message_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
                        data = (time, sender_id,receiver_id, message_type,media_content,text_content,message_id)
                        cursor.execute(insert_query, data)
        except:
            pass


class DbUtil_group(DbUtil_util):

    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS group_chat (id INTEGER PRIMARY KEY, time TEXT NOT NULL,group_id TEXT NOT NULL, sender_id TEXT NOT NULL,message_type INT,media_content TEXT NOT NULL,text_content TEXT NOT NULL,message_id TEXT NOT NULL,reply_to TEXT);"
        cursor.execute(create_table_sql)

    def insert_data(self,cursor, entity_list, data_list):

        for i in range(len(entity_list)):
            if len(data_list[i]) == 0:
                continue
            else:
                for j in range(len(data_list[i])):
                    time = data_list[i][j]['time']
                    group_id = entity_list[i].id
                    #group_name = f"{entity_list[i].title or ''}"
                    sender_id = data_list[i][j]['sender_id']
                    message_type = data_list[i][j]['message_type']
                    media_content = f"{data_list[i][j]['media_content'] or ''}"
                    text_content = f"{data_list[i][j]['text_content'] or ''}"
                    message_id = data_list[i][j]['message_id']
                    reply_to = f"{data_list[i][j]['reply_to'] or ''}"
                    insert_query = f"INSERT INTO group_chat (time,group_id,sender_id, message_type,media_content,text_content,message_id,reply_to) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
                    data = (time,group_id, sender_id, message_type,media_content, text_content, message_id, reply_to)
                    cursor.execute(insert_query, data)

class DbUtil_channel(DbUtil_util):

    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS channel_broast (id INTEGER PRIMARY KEY, time TEXT NOT NULL,channel_id TEXT, sender_id TEXT,message_type INT,media_content TEXT, text_content TEXT,message_id TEXT);"
        cursor.execute(create_table_sql)

    def insert_data(self,cursor, entity_list, data_list):

        for i in range(len(entity_list)):
            if len(data_list[i]) == 0:
                continue
            else:
                for j in range(len(data_list[i])):
                    time = data_list[i][j]['time']
                    channel_id = entity_list[i].id
                    #channel_name = f"{entity_list[i].title or ''}"
                    sender_id = data_list[i][j]['sender_id']
                    message_type = data_list[i][j]['message_type']
                    media_content = f"{data_list[i][j]['media_content'] or ''}"
                    text_content = f"{data_list[i][j]['text_content'] or ''}"
                    message_id = data_list[i][j]['message_id']
                    insert_query = f"INSERT INTO channel_broast (time, channel_id, sender_id,message_type, media_content, text_content, message_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
                    data = (time, channel_id, sender_id, message_type,media_content,text_content,message_id)
                    cursor.execute(insert_query, data)


#个人信息
class DbUtil_selfinfo():
    def __init__(self, save_path=None, userinfo=None):
        self.save_path= save_path
        self.userinfo = userinfo


    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS user_info (id INTEGER PRIMARY KEY, name TEXT , user_id TEXT ,user_name TEXT ,phone_number TEXT);"
        cursor.execute(create_table_sql)

    def insert_data(self,cursor, userinfo):
        name = f"{userinfo.last_name or ''}{'-' if userinfo.last_name and userinfo.first_name else ''}{userinfo.first_name or ''}"
        user_id= userinfo.id
        user_name = f"{userinfo.username or ''}"
        phone_number=f"{userinfo.phone or ''}"
        insert_query = f"INSERT INTO user_info (name, user_id, user_name, phone_number) VALUES (?, ?, ?, ?);"
        data = (name, user_id,user_name, phone_number)
        cursor.execute(insert_query, data)
        pass

    def run(self):
        try:
            db_name = str(self.userinfo.id) + '.db'
            db_path = os.path.join(self.save_path, db_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            self.create_table(cursor)
            self.insert_data(cursor, self.userinfo)
            conn.commit()
            conn.close()
        except:
            pass

#实体信息-群得加个描述
class DbUtil_entityinfo():

    def __init__(self, save_path=None, userinfo=None, dialog=None):
        self.save_path = save_path
        self.userinfo = userinfo
        self.dialog = dialog

    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS entity_info (id INTEGER PRIMARY KEY,  entity_id TEXT ,entity_name TEXT ,entity_username TEXT,entity_type INT ,info TEXT);"
        cursor.execute(create_table_sql)

    def insert_data(self, cursor, entity):
        for i in range(len(entity)):
            if hasattr(entity[i], 'full_chat'):
                entity_id = entity[i].full_chat.id
                if entity[i].full_chat.migrated_from_chat_id:
                    entity_id = entity[i].full_chat.migrated_from_chat_id
                entity_name = f"{entity[i].chats[0].title or ''}"
                entity_type = 2
                entity_desc = f"{json.dumps(entity[i].full_chat.about) or ''}"
                entity_username = f"{entity[i].chats[0].username or ''}"
            else:
                if isinstance(entity[i], types.User):
                    entity_name = f"{entity[i].last_name or ''}{'-' if entity[i].last_name and entity[i].first_name else ''}{entity[i].first_name or ''}"
                    entity_type = 1
                    entity_desc = ''
                    entity_id = entity[i].id
                    entity_username = f"{entity[i].username or ''}"


                elif isinstance(entity[i], types.Channel):
                    entity_name = f"{entity[i].title or ''}"
                    entity_type = 3
                    entity_desc = ''
                    entity_id = entity[i].id
                    entity_username = f"{entity[i].username or ''}"

            insert_query = f"INSERT INTO entity_info (entity_id, entity_name, entity_username,entity_type ,info) VALUES (?, ?, ? ,? ,?);"
            data = (entity_id, entity_name,entity_username, entity_type, entity_desc)
            cursor.execute(insert_query, data)


    def run(self):
        try:
            db_name = str(self.userinfo.id) + '.db'
            db_path = os.path.join(self.save_path, db_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            self.create_table(cursor)
            self.insert_data(cursor, self.dialog)
            conn.commit()
            conn.close()
        except:
            pass


#群成员
class DbUtil_groupparticipant():
    def __init__(self, save_path=None, userinfo=None, participant_list=None):
        self.save_path = save_path
        self.userid = userinfo
        self.participant_list = participant_list


    def create_table(self,cursor):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS group_member (id INTEGER PRIMARY KEY, group_id TEXT , user_id TEXT,name TEXT ,user_name TEXT ,is_admin int);"
        cursor.execute(create_table_sql)



    def insert_data(self,cursor, participant_list):
        for i in range(len(participant_list)):
            if len(participant_list[i]) == 0:
                continue
            else:
                for j in range(len(participant_list[i])):
                    group_id = participant_list[i][j]['group_id']
                    user_id = participant_list[i][j]['user_id']
                    name = participant_list[i][j]['name']
                    user_name = participant_list[i][j]['username']
                    is_admin = participant_list[i][j]['is_admin']
                    insert_query = f"INSERT INTO group_member (group_id, user_id, name, user_name, is_admin) VALUES (?, ?, ?, ?, ?);"
                    data = (group_id, user_id, name, user_name, is_admin)
                    cursor.execute(insert_query, data)
                    pass

    def run(self):
        try:
            db_name = str(self.userid) + '.db'
            db_path = os.path.join(self.save_path, db_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            self.create_table(cursor)
            self.insert_data(cursor, self.participant_list)
            conn.commit()
            conn.close()
        except:
            pass


if __name__ == '__main__':
    save_path = ''
    me = User(id=12345, is_self=False, contact=True, mutual_contact=False, deleted=False, bot=False, bot_chat_history=False, bot_nochats=False, verified=False, restricted=False, min=False, bot_inline_geo=False, support=False, scam=False, apply_min_photo=True, fake=False, bot_attach_menu=False, premium=False, attach_menu_enabled=False, bot_can_edit=False, close_friend=False, stories_hidden=False, stories_unavailable=True, access_hash=-6666798093269235205, first_name='昊', last_name='张', username=None, phone='8613506695699', photo=None, status=UserStatusRecently(), bot_info_version=None, restriction_reason=[], bot_inline_placeholder=None, lang_code=None, emoji_status=None, usernames=[], stories_max_id=None, color=None, profile_color=None)
    print(me.id)


    a = [[{'group_id': 2151561346, 'user_id': 5701630718, 'name': 'Hxhs-Dhdb', 'username': '', 'is_admin': 1},
      {'group_id': 2151561346, 'user_id': 5019471989, 'name': 'Z-Z', 'username': 'gxt_testname', 'is_admin': 1}]]
    group_chat_history = [
    ]

    #DbUtil_groupparticipant(save_path,123,a).run()
    #DbUtil_entityinfo(save_path, me, dialog_info).run()



