# encoding: utf8
from bs4 import BeautifulSoup
import requests
import json
import re

class JD:
    """
    开发者：
    商品id及sku(从商品页获取)：100009083152
    商品详细页：https://item.m.jd.com/product/100009083152.html
    预售商品价格接口：https://yuding.jd.com/presaleInfo/getPresaleInfo.action?callback=yushouNoWayJDCBA&sku=100009083152 
    商品配置接口：https://yx.3.cn/service/info.action?ids=100009083154
    实现功能：输入商品链接，输出当前商品价格。
    用户：输入 链接 , 输出价格,若为预售商品则输出预售商品价格
    """
    def __init__(self,goodsUrl):
        self.shopId = self._url(goodsUrl) # 防止输入数字
        self.urlPrice = 'https://item.m.jd.com/product/%s.html'%self.shopId
        self.urlysPrice = 'https://yuding.jd.com/presaleInfo/getPresaleInfo.action?callback=yushouNoWayJDCBA&sku=%s'%self.shopId
        self.urlConfig = 'https://yx.3.cn/service/info.action?ids=%s'%self.shopId
        self.headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
}
    def _url(self,shopUrl):
        """返回：商品 id """
        try:
            temp = re.findall(r'product/(\d+).html', shopUrl) # 手机端链接
            if temp:
                pid = temp[0]
            else:
                pid = re.findall(r'jd.com/(\d+).html', shopUrl)[0] # pc 端链接
        except IndexError as e:
            raise IndexError('请检查 1 是否为京东商品链接，2 链接中需含有 product/ 字段。%s.'%e)
        return pid

    def price(self) -> float or None:
        """返回：商品价格"""
        try:
            r = requests.get(self.urlPrice,headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('jd commodity now price error', e)
            return False
        soup = BeautifulSoup(r.text, features="lxml")
        result = soup.find(class_="price large_size")
        price = result.text.strip().replace('¥','') # 获取价格
        return float(price)


    def ysPrice(self) -> float or None:
        """返回：预售商品价格 """
        try:
            r = requests.get(self.urlysPrice,headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('jd commodity presell price error', e)
            return False
        result = r.text[17:-1] # 去除首尾不需要的字符串
        # print('输出看看',result)
        result = json.loads(result)
        if 'error' not in result:
            price = result['ret']['currentPrice'] # 价格 
        else:
            print('你输入的商品非预售商品')
            return False
        return float(price)

    def config(self):
        """返回：商品标题"""
        try:
            r = requests.get(self.urlConfig,headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('jd commodity configure error', e)
            return False
        result = r.json()
        name = result[self.shopId]['name'] # 配置信息
        return name

    def main(self):
        title = self.config()
        price = self.ysPrice()
        if not price:
            price = self.price()
        return title,price

if __name__ == '__main__':
    goodsurl = 'https://item.m.jd.com/product/10873703488.html?sku=10873703488'    
    jd = JD(goodsurl) # 测试 id：100009083152 商品：联想 y9000x 笔记本电脑 2 热水壶
    title,price = jd.main()
    print('标题 %s, 价格 %s.'%(title, price))

