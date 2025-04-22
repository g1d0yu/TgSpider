
if __name__ == '__main__':
    # try:
    import argparse
    import time
    from utils import Schedule
    # except:
    #     print('请启用虚拟环境')
    tdata_path = r"D:\Telegram Desktop\tdata"
    #tdata_path1 = r"D:\Program Files\Telegram Desktop\tdata"
    proxy = ('http', '127.0.0.1', 7890)

    try:
        parser = argparse.ArgumentParser(description='-h使用帮助')
        parser.add_argument('-path', required=True, help='tdata文件夹路径')
        parser.add_argument('-proxy', help='字符串')

        time_start = time.time()
        #args = parser.parse_args()

        args = parser.parse_args(['-path', tdata_path, '-proxy', proxy])

        schedule = Schedule()
        schedule.check_args(args)
        schedule.get_start()
        time_end = time.time()  # 记录结束时间
        time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
        print('总耗时：',time_sum)
    except:
        pass


