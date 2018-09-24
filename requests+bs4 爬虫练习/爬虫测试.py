import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

url = 'https://cn.vjudge.net/contest/229338#overview'
# url = 'https://www.baidu.com'
r = requests.Session()
kv = {'user-agent':'Mozilla/5.0'} #伪装成火狐浏览器
try:
    r = requests.get(url,headers = kv)
    r.raise_for_status()
    r = requests.get(url = 'https://cn.vjudge.net/contest/229338#problem/A',headers = kv)
    soup = BeautifulSoup(r.text,'html.parser')
    print(soup.prettify())
except:
    print('失败')
