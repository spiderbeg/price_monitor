# encoding:utf8
import requests
import json
import re

class SN:
    """
    功能：在商品详细页显示商品已选的条件下。输入商品链接，获取苏宁易购商品价格 
    商品详细页链接：https://m.suning.com/product/0070074466/646336020.html # 这里分别为 id id2
    商品信息接口：https://pas.suning.com/nsenitemsale_000000000646336020_0070074466_5_999_100_025_0250199______1000173_.html?_=1571284815051&callback=wapData
    
    """
    def __init__(self,goodsUrl):
        self.shopId,self.shopId2 = self._url(goodsUrl)
        self.url = 'https://pas.suning.com/nsenitemsale_0000000%s_%s_5_999_100_025_0250199______1000173_.html?_=1571284185922&callback=wapData'%(self.shopId2,self.shopId)
        self.headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',}
        self.result = self._info()

    def _url(self, goodsUrl) -> (str,str):
        """从输入链接中获取能确定商品的 id
        输入：商品链接；
        返回：商品 id 元组
        """
        try:
            result = re.findall(r'com/product/(\d.+).html', goodsUrl)
            if not result:
                result = re.findall(r'suning.com/(\d.+).html', goodsUrl)
            result2 = result[0].split(r'/')
        except IndexError as e:
            raise IndexError('请检查 1 是否为苏宁易购商品链接，2 链接中需含有 product 字段。%s.'%e)
        # print(result2)
        if len(result2[1]) == 18:
                result2[1] = result2[1][7:]
        return result2[0],result2[1]

    def _info(self):
        """请求返回的商品信息
        返回：含商品信息的 json 数据
        """
        try:
            r = requests.get(self.url, headers=self.headers)
            result = r.text.strip()[8:-1]
        except requests.exceptions.RequestException as e:
            print('信息请求错误，请检查 id', e)
            return None
        result = json.loads(result)
        return result

    def config(self):
        """返回：商品标题"""
        try:
            title = self.result['data']['data1']['data']['itemInfoVo']['itemDisplayName']
        except KeyError as e:
            print('标题名取值键值错误，请检查', e)
            return None            
        return title
    
    def price(self) -> float or None:
        """返回：商品单价"""
        try:
            price = self.result['data']['price']['saleInfo'][0]['promotionPrice']
        except KeyError as e:
            print('价格取值键值错误，请检查', e)
            return None            
        return float(price)
    def tPrice(self) -> float or None:
        """返回：商品的团购价"""
        try:
            price = self.result['data']['price']['saleInfo'][0]['pgPrice']
        except KeyError as e:
            print('团购价格取值键值错误，请检查', e)
            return None           
        if price: 
            return float(price)
        else:
            return None

    def main(self):
        price = self.price() # 非团购价
        tuanPrice = self.tPrice() # 团购价
        title = self.config()
        if tuanPrice:
            return title,tuanPrice
        else:
            return title,price


if __name__ == "__main__":
    goodsurl = 'https://m.suning.com/product/0000000000/000000010606656191.html'
    # goodsurl = 'https://product.suning.com/0000000000/11128387984.html?srcPoint=dacu_ghpc2019_20190703205229104145_01&safp=d488778a.ghpc2019.20190703205229104145.4&safc=prd.0.0'
    sn = SN(goodsurl)
    title,price = sn.main()
    print('标题 %s, 价格 %s. '%(title,price))