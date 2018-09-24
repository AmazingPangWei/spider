from bs4 import BeautifulSoup
import requests

# url = "https://python123.io/ws/demo.html"
# demo = requests.get(url)
demo = '<div class="card-list"><div class="card m-panel card42"><div class="card-wrap"><div class="card-main"><div class="m-box"><div class="box-left m-box-col m-box-center-a"><!-- --> <span class="link-text"><span class="main-link">账号信息</span></span></div> <div class="box-right m-box-center-a"><!-- --> <!-- --></div></div></div></div></div><div class="card m-panel card41" data-v-3dab69b2=""><div class="card-wrap" data-v-3dab69b2=""><div class="card-main" data-v-3dab69b2=""><div class="data-row" data-v-3dab69b2=""><div class="m-box" data-v-3dab69b2=""><!-- --> <!-- --> <!-- --> <div class="box-left" data-v-3dab69b2="">昵称</div> <div class="box-main m-box-col" data-v-3dab69b2="">赵雷Z</div> <!-- --> <!-- --></div></div></div></div></div><div class="card m-panel card41" data-v-3dab69b2=""><div class="card-wrap" data-v-3dab69b2=""><div class="card-main" data-v-3dab69b2=""><div class="data-row" data-v-3dab69b2=""><div class="m-box" data-v-3dab69b2=""><!-- --> <!-- --> <div class="box-left" data-v-3dab69b2=""><span class="m-auth-yellowv" data-v-3dab69b2="">微博认证</span></div> <!-- --> <div class="box-main m-box-col" data-v-3dab69b2="">民谣歌手赵雷</div> <!-- --> <!-- --></div></div></div></div></div><div class="card m-panel card41" data-v-3dab69b2=""><div class="card-wrap" data-v-3dab69b2=""><div class="card-main" data-v-3dab69b2=""><div class="data-row" data-v-3dab69b2=""><div class="m-box" data-v-3dab69b2=""><!-- --> <!-- --> <!-- --> <div class="box-left" data-v-3dab69b2="">简介</div> <div class="box-main m-box-col" data-v-3dab69b2="">工作请洽：zlmusic@vip.163.com 微博：@小齐不冥想</div> <!-- --> <!-- --></div></div></div></div></div> <!-- --></div>'
soup = BeautifulSoup(demo,"html.parser")
#prettify 优化结果
print(soup.prettify())

