import requests
import os

url='http://pic1.win4000.com/wallpaper/f/55dd60fe5041c.jpg'
root = 'D://python//spider//'
path = root + url.split('/')[-1][-15:]
print(path)
try:
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        kv = {'user-agent':'Mozilla/5.0'} #伪装成火狐浏览器
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        with open(path,'wb') as f:
            # r.content是二进制编码
            f.write(r.content)
            print('文件写入')
    else:
        print('文件已存在')
except:
    print("爬取失败")