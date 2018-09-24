import requests
from bs4 import BeautifulSoup
import bs4
requests.packages.urllib3.disable_warnings()


def getHTMLText(url):
    try:
        id = "1832394515@qq.com"
        ps = "74520tsy"
        post = {
            'user_name': id,
            'password': ps
        }
        r = requests.Session()
        s = r.post('https://www.ctguqmx.com/account/ajax/login_process/', data=post, verify=False)
        s = r.post(url='https://www.ctguqmx.com/qiandao')
        # print(s.text)
        r = r.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def toList(list,html):
    soup = BeautifulSoup(html,'html.parser')
    for x in soup.find('tbody').children:
        #正确的元素
        if isinstance(x, bs4.element.Tag):
            #按td分开
            temp = x('td')
            if(temp.__len__()==0):
                break
            sign=[]
            sign.append(temp[0].string)
            sum=1
            day=0;
            while sum<=21:
                t = temp[sum].attrs
                if 'id' in t:
                    day+=1
                if sum%3==0:
                    sign.append(day)
                    day=0
                sum+=1
            sign.append(temp[22].string)
            list.append(sign)
def printList(list):
    t = "{0:{9}^4}\t{1:{10}^3}\t{2:{11}^3}\t{3:{12}^3}\t{4:{13}^3}\t{5:{14}^3}\t{6:{15}^3}\t{7:{16}^3}\t{8:{17}^4}\t"
    print(t.format("姓名","星期一","星期二","星期三","星期四","星期五","星期六","星期天","签到次数",chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288)))
    for x in range(list.__len__()):
        print(t.format(list[x][0],list[x][1], list[x][2],list[x][3],list[x][4],list[x][5],list[x][6],list[x][7],list[x][8],chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288),chr(12288)))

def main(url):
    html = getHTMLText(url)
    list=[]
    toList(list,html)
    printList(list)


url = 'http://172.25.1.105/index.php/Qiandao/showinfo'

main(url)
