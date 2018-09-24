import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import  time
import json

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import datetime

starttime = datetime.datetime.now()

#long running



#全局设置
#driver = webdriver.Firefox()
#
#不要浏览器显示出来
options = webdriver.FirefoxOptions()
options.set_headless()
options.add_argument('--disable-gpu')
driver=webdriver.Firefox(firefox_options=options)

#设置一下延迟，延迟越低，越不稳定！
delay = 3

#获取html文本,设置翻页次数
def get_html(url):
    driver.get(url)
    time.sleep(5)
    element = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[3]/div[1]/div[1]')
    element.click()
    time.sleep(3)

#获取页面信息
def get_user_data(text):
    time.sleep(1)
    soup = BeautifulSoup(text,'html.parser')
    res = []
    t_soup = soup.find_all(attrs={'class': 'data-row'})
    #key=box-left
    #value=box-main
    #对于每一个data-row设为x：
    for x in t_soup:
        for child in x.children:
            key = child.find(attrs={'class':'box-left'}).string
            value = child.find(attrs={'class':'box-main'}).string
            res.append({key:value})
    return res
#获得真正的链接
def get_real_url(str):
    url = str
    url = url.split('/')[-1]
    t = 'https://m.weibo.cn/u/{0}?uid={0}'
    to = t.format(url)
    return to

def make_back():
    driver.back()
    driver.back()
#获得主页面信息
def get_data(url):
    driver.get(url)
    # 进入主页
    time.sleep(0.5*delay)
    # 切换页面
    driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[2]/nav/div/div/div/ul/li[1]/span').click()
    time.sleep(0.5*delay)

    js = "document.documentElement.scrollTop=300"  # 拖动滚动条到屏幕底端
    driver.execute_script(js)
    # 进入基本资料
    #不停尝试访问
    time.sleep(0.5 * delay)
    url_t = '/html/body/div/div[1]/div[2]/div[3]/div/div/div[{0}]/div/div/a'
    i=2
    while 1:
        try:
            url_xpath = url_t.format(str(i))
            driver.find_element_by_xpath(url_xpath).click()
            break
        except:
            i+=1
            if i>=100:
                break
            continue
    res = get_user_data(driver.page_source)
    make_back()
    return res
#获得发文人的信息
def get_poster_data():
    say = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/article/div/div/div[1]').text
    url = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/div/div/header/div[1]/a').get_attribute('href')
    url = get_real_url(url)
    res = get_data(url)
    res.append({'text': say})
    print("已抓取发微博者信息！")
    return res

#获得转发数据
#开始处理转发消息 num为消息条数
def get_comment(num):
    user_text = '/html/body/div/div[1]/div/div[3]/div[2]/div[{0}]/div/div/div/div/div/div[1]/div/div/h3'
    image = '/html/body/div/div[1]/div/div[3]/div[2]/div[{0}]/div/div/div/div/a/div'
    res = []
    #一次性获得所有用户的url与评论
    url_set=[]
    comment_set=[]
    i = 1
    try:
        while i<=num:
            text_xpath = user_text.format(i)
            image_xpath = image.format(i)
            comment_set.append(driver.find_element_by_xpath(text_xpath).text)
            distence = 122 * (i-1)
            js = "document.documentElement.scrollTop="+str(distence)  # 拖动滚动条到屏幕底端
            driver.execute_script(js)
            #防止消息过长，检测不出对应的xpath
            while 1:
                try:
                    driver.find_element_by_xpath(image_xpath).click()
                    break
                except:
                    i+=1
                    distence = 122 * (i - 1)
                    js = "document.documentElement.scrollTop=" + str(distence)  # 拖动滚动条到屏幕底端
                    driver.execute_script(js)
                    continue
            url = get_real_url(driver.current_url)
            driver.back()
            time.sleep(0.3*delay)
            url_set.append(url)
            i+=1
    except:
        print("可能因为网速原因，抓取数据不足！")
    #根据已经抓到的url遍历
    print("已抓取完url,共有"+str(len(url_set))+"条url!")
    for i in range(len(url_set)):
        try:
            t = get_data(url_set[i])
            t.append({'text':comment_set[i]})
            res.append(t)
            print("抓取第"+str(i+1)+'条！')
        except:
            print("本次抓取失败!")

    return res

#需要爬取的微博
url = "https://m.weibo.cn/status/4033487356638762"

#访问爬取网页
get_html(url)
res=[]
#获得发文人的信息
res.append(get_poster_data())
res.append(get_comment(100))
#ensure_ascii：默认值True，如果dict内含有non-ASCII的字符，则会类似\uXXXX的显示数据，设置成False后，就能正常显示
json_data = json.dumps(res,sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
print(json_data)
with open('json_data.json','w',encoding='utf-8') as f:
    f.write(json_data)
endtime = datetime.datetime.now()

print ((endtime - starttime).seconds)