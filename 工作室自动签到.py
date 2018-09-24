import requests

requests.packages.urllib3.disable_warnings()
id = "你的账号"
ps = "你的密码"
post = {
    'user_name':id,
    'password':ps
    }
# header = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
#     'Host': 'www.ctguqmx.com'
# }
r= requests.Session()
s = r.post('https://www.ctguqmx.com/account/ajax/login_process/',data=post,verify=False)

s = r.post(url = 'https://www.ctguqmx.com/qiandao')
# print(s.text)

s = r.post(url = 'http://172.25.1.105/index.php/Qiandao/doQd')
print(s.text)