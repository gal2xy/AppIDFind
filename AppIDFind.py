import js2py
import requests
from bs4 import BeautifulSoup


class AppIdFind:
    url = "https://mp.weixin.qq.com/wxawap/waverifyinfo"
    action = "get"
    AppIdKey = "appid"
    appidlen = 16
    params = {
        "action": "get",
        "appid": None,
    }
    headers = {}
    cookies = {}

    # 可能是共享设备小程序的标签
    lables = ["充电服务", "骑车", "租车", "共享服务"]# "生活缴费"


    //不建议爆破，会被检测到
    def enumerateSharedDeviceApp(self):

        # 16位的十六进制数!!!
        for partappid in range(991742836697384182, 991742836697387182):
            appid = "wx" + str(hex(partappid)[2:].zfill(self.appidlen))
            self.findAppByAppId(appid)

    def findAppByAppId(self, appid: str):
        self.params[self.AppIdKey] = appid
        responseResult = requests.get(self.url, headers=self.headers, params=self.params)
        html = responseResult.text

        # 使用BeautifulSoup解析HTML页面
        soup = BeautifulSoup(html, "html.parser")
        script_tags = soup.find_all("script")

        # 提取脚本
        windowcgiDataString = script_tags[2].text
        # print(windowcgiDataString)

        # 提取category_list属性的值
        try:
            # 执行js脚本得到json数据
            # 放在try中执行,因为服务类目有为空的,会导致报错
            windowcgiData = js2py.eval_js(windowcgiDataString)
            # 含众多标签
            labels = windowcgiData["category_list"]["cate"]
            # print(labels)
            for label in labels:
                if label in self.lables:
                    # 记录 小程序名
                    print(f'所属企业: {windowcgiData["name"]}, 小程序名: {windowcgiData["nickname"]}, 服务类目: {windowcgiData["category_list"]}')
                    break
        except:
            # print("服务类目为空")
            pass


if __name__ == "__main__":
    appidfind = AppIdFind()
    appidfind.findAppByAppId("wx0dc360db01e2c4f6")