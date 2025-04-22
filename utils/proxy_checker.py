import requests

url = 'https://www.google.com'
def check_proxy(proxy):
    try:
        if len(proxy)>0:
            proxy = {
                'http': 'http://{}:{}'.format(proxy[1], proxy[2]),
                'https': 'http://{}:{}'.format(proxy[1], proxy[2])
            }
        else:
            proxy = None
        response = requests.get(url, proxies=proxy)
        # 检查代理的可用性
        if response.status_code == 200:
            #print('网络环境检查成功')
            return True
        else:
            return False
    except :
        print('网络环境不可达，请检查网络或代理')
        pass
if __name__ == '__main__':
    check_proxy(proxy=('http', '127.0.0.1', 7890))
