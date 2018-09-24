import requests
def GetWeb(keyword):
    try:
        kv={'wd':keyword}
        r=requests.get('http://www.baidu.com/s',params=kv)
        # 状态码不是200，则抛出错误
        print(r.request.url)
        print(len(r.text))
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text[:1000]
    except:
        return '访问错误'

keyword = 'python'
GetWeb(keyword)