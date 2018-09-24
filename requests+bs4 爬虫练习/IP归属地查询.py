import requests

url = "http://m.ip138.com/ip.asp?ip="
ip='119.75.216.20'
try:
    r=requests.get(url+ip)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    print(r.text[-500:])
except:
    print("获取失败")
