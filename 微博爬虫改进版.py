import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from requests.cookies import RequestsCookieJar

#从这里输入您想要的爬取的url
weibo_url = 'https://weibo.com/1034616531/F1wTluh0k?filter=hot&root_comment_id=0&type=comment#_rnd1539606831195'
#输入你想爬取的页数，-1为默认最大爬取页数
max_page_num = 2

#记录uid和text的list
id_and_text= []

#获取时间戳的时间
def get_timestamp(now_time):
    date = now_time
    date = date[:10]
    return int(date)

#第一次访问，获取微博id，并把cookies存下来，方便之后的get请求
def do_first(url):
    print("初始化中......")
    #driver = webdriver.Firefox()
    # 不要浏览器显示出来
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(15)
    #处理链接不一样的情况
    error_time = 0
    while driver.current_url == 'https://weibo.com/login.php' or driver.current_url == "https://weibo.com/":
        if error_time==3:
            print("请重试，链接失误太多！")
            driver.close()
            exit(0)
        print("初始化失败，开始重试...")
        driver.get(url)
        time.sleep(15)
        error_time+=1
    #获得id
    print("初始化完成！")
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    t = soup.find(attrs={"class":"WB_from S_txt2"})
    id = t.findChild('a').get("name")
    t_time = t.findChild('a').get('date')
    #获得text、uid、时间t
    dic = {}
    text = soup.find(attrs={"class":"WB_text W_f14"}).get_text()
    uid = t.findChild('a').get("href").split('/')[1]
    dic['uid'] = uid
    dic['text'] = text
    dic['t'] = get_timestamp(t_time)
    dic['id'] = id
    id_and_text.append(dic)

    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as f:
        json.dump(cookies, f)
    driver.close()
    print("已将cookies写入，并返回该条微博的id")
    return id

#获取之前的cookies
def get_cookies():
    jar = RequestsCookieJar()
    with open("cookies.txt", "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
    print("已获取cookies！")
    return jar
def get_user_info(user_list):
    res = []
    r = requests.session()
    for user in user_list:

        user_info_params = {
            "type": "uid",
            "value": user['uid']
        }
        try:
            s = r.get('https://m.weibo.cn/api/container/getIndex', params=user_info_params)
            json_data = json.loads(s.text)
            json_data = json_data['data']['userInfo']
            json_data['original_text'] = user['text']
            json_data['t'] = user['t']
            json_data['id'] = str(user['id'])
            json_data['uid'] = user['uid']
            res.append(json_data)
            print("id号为" + user_info_params["value"] + "的用户抓取成功！")
        except:
            print("id号为"+user_info_params["value"]+"的用户抓取失败！")
    return res

def get_user_id(url):
    return url.split('=')[1]
#解析html页面
def parse_html(text):

    soup = BeautifulSoup(text, "html.parser")
    soup = soup.find_all(attrs={'class': 'list_li S_line1 clearfix'})
    #抓取t,text,uid
    for s in soup:
        dic = {}
        id = s.get('mid')
        a = s.find('a',attrs={'node-type': 'name'})
        t = s.find('a',attrs={'class':'S_txt1','node-type':'feed_list_item_date'})
        user_text = s.find('span',attrs={'node-type':'text'})
        dic['uid'] = get_user_id(a.get('usercard'))
        dic['text']= user_text.get_text()
        dic['t'] = get_timestamp(t.get('date'))
        dic['id'] = id
        id_and_text.append(dic)

def get_user_id_and_text(url):
    id = do_first(url)
    jar = get_cookies()
    #伪装成firefox浏览器
    header={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection":"keep-alive",
    "Host":"weibo.com",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:62.0) Gecko/20100101 Firefox/62.0"
    }
    #参数
    params={
        'id': id,
        'page':'1',
    }

    #解析第一页
    r = requests.session()
    max_page = 0
    try:
        s = r.get('https://weibo.com/aj/v6/mblog/info/big',headers = header,params=params,cookies=jar)
        json_data = json.loads(s.text)
        max_page = json_data['data']['page']['totalpage']
        html = json_data['data']['html']
        parse_html(html)
    except:
        print("转发第1页抓取失败！强制退出！")
        exit(0)
    print("转发第1页抓取成功")
    #解析2~max页面
    if max_page_num != -1:
        max_page = max_page_num
    for i in range(2, max_page + 1):
        params = {
            'id': id,
            'page': str(i),
        }
        try:
            s = r.get('https://weibo.com/aj/v6/mblog/info/big', headers=header, params=params, cookies=jar)
            json_data = json.loads(s.text)
            html = json_data['data']['html']
            parse_html(html)
            print("转发第" + params['page'] + "页抓取成功！")
        except:
            print("转发第"+params['page']+"页抓取失败！")

def to_json_file(res):
    json_data = json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open('json_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

if __name__ == '__main__':
    get_user_id_and_text(weibo_url)
    print("开始抓取用户信息！")
    res = get_user_info(id_and_text)
    to_json_file(res)
    print("爬取完成!")