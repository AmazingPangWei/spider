from bs4 import BeautifulSoup
import requests
import re
url = "https://python123.io/ws/demo.html"
demo = requests.get(url).text

soup = BeautifulSoup(demo,"html.parser")

# 包涵a标签
print(soup.find_all('a'))
print(soup.find_all().find_all)
# 包涵a,b标签
for x in soup.find_all(['a','b']):
    print(x)
#p标签中有course属性
for x in soup.find_all('p','course'):
    print(x)

#id为link1的标签
print(soup.find_all(id='link1'))

#结合正则表达式
print(re.compile('python'))
print(soup(string = re.compile('python')))