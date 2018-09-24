import requests
def GetWeb(url):
    try:
        r=requests.get(url,timeout=30)
        # 状态码不是200，则抛出错误
        print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text[:1000]
    except:
        return '访问错误'


GetWeb('https://www.amazon.cn/gp/product/B01M8L5Z3Y')
