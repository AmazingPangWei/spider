import requests
from bs4 import BeautifulSoup
import bs4
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
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
            list.append([ temp[0].string,temp[1].string,temp[2].string ])
def printList(list,num):
    t = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(t.format("排名","大学名称","总分",chr(12288)))
    for x in range(num):
        print(t.format(list[x][0],list[x][1], list[x][2], chr(12288)))

def main():
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2018.html'
    #爬取前max名大学
    max = 300
    html = getHTMLText(url)
    list=[]
    toList(list,html)
    printList(list,300)

main()