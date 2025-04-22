import os
import shutil
from datetime import datetime

import pytz
from opentele.td import TDesktop


from utils.config import getconf
from utils.recoder import RecoderUtil

from utils.user_info import UserInfo
from .utilstool import _format_path, _format_proxy
from .path_checker import check_path
from .proxy_checker import check_proxy
from .session import Session
from .aiosqlcrawl import AiodbSession
from .separatecrawl import SeparateSession

class ClientFactory:
    @staticmethod
    def create_separate_client(tdesk, proxy):
        return SeparateSession(tdesk, proxy).run()

    @staticmethod
    def create_stream_client(tdesk, proxy):
        return AiodbSession(work_path=tdesk, proxy=proxy).run()

    @staticmethod
    def create_incremental_client(tdesk, proxy, last_time):
        return Session(work_path=tdesk, proxy=proxy, last_time=last_time).run()

class Schedule():

    def __init__(self):
        self._worklist = []
        self._proxy = None
        self.limit = 100
        self.max_file_size = 1024

    def getconf(self):
        conf_dict = getconf('config.ini')
        for key, value in conf_dict.items():
            if key == 'limit':
                if value.lower() == 'none':
                    self.limit = None
                else:
                    self.limit = int(value)
            elif key == 'max_size':
                if value.lower() == 'none':
                    self.max_file_size = None
                else:
                    self.max_file_size = int(value)

    def check_args(self,args):
        try:
            path = _format_path(args.path)
            self.tdata_path = path
            self._proxy = _format_proxy(args.proxy)
            if check_proxy(self._proxy) is not True:
                print('网络环境不可达，请检查网络或代理')
                exit(0)
            self._worklist = check_path(path)
            if len(self._worklist) == 0:
                print('检查提供的tdata目录有可用账户')
                exit(0)
        except:
            pass

    def get_start(self):
        print("当前目录共发现{}个有效账户".format(len(self._worklist)))
        for i,work_path in enumerate(self._worklist):
            print('=========================================')
            print('开始获取第{}个用户'.format(i+1))
            try:
                recoder = RecoderUtil()
                user = TDesktop(work_path)
                user_id = user.accounts[i].UserId

                last_time = recoder.get_last_run_time(user_id)
                now_time = datetime.today().replace(microsecond=0).astimezone(pytz.utc)

                if last_time == None:
                    self.getconf()
                    if (self.limit < 100000) and (self.max_file_size < 102400):
                        ClientFactory.create_separate_client(work_path, self._proxy)
                    else:
                        ClientFactory.create_stream_client(work_path, self._proxy)
                else:
                    last_time = datetime.fromisoformat(last_time)
                    ClientFactory.create_incremental_client(work_path, self._proxy, last_time)
                recoder.update_last_run_time(TDesktop(work_path).accounts[i].UserId,now_time)
            except:
                print('error')
                pass
            print('第{}个账户执行结束'.format(i+1))
            print('=========================================')
            shutil.rmtree(work_path)



if __name__ == '__main__':

    pass