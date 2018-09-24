import requests
import re
import scrapy
def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""
def parsePage(l,html):
    price =  re.findall(r'"view_price":"([\d\.]*)"',html)
    name = re.findall(r'"raw_title":".*?"',html)

    for x in range(len(price)):
        p = eval(price[x].split(':')[1])
        n = eval(name[x].split(':')[1])
        l.append([p,n])
def printGoodsList(l):
    template = '{0:^6}\t{1:^12}\t{2:{3}^16}'
    print(template.format("序号","价格","名称",chr(12288)))
    cnt=0
    for x in l:
        cnt+=1
        print(template.format(cnt,x[0],x[1],chr(12288)))
def main():
    goods='scrapy'
    deepth=4
    start_url='https://s.taobao.com/search?q='
    url = start_url+goods
    infolist=[]
    for i in range(deepth):
        try:
            url = url+'&s='+str(i*44)
            html=getHTMLText(url)
            parsePage(infolist,html)
        except:
            continue
    printGoodsList(infolist)
main()
