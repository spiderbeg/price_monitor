# encoding:utf8
import requests
import json
import re

class SN:
    """
    在商品详细页显示商品已选的条件下。传入链接或其中两个id，获取苏宁易购商品价格 
    商品详细页链接：https://m.suning.com/product/0070074466/646336020.html # 这里分别为 id id2
    商品信息接口：https://pas.suning.com/nsenitemsale_000000000646336020_0070074466_5_999_100_025_0250199______1000173_.html?_=1571284815051&callback=wapData
    """
    def __init__(self,goodsUrl):
        self.shopId,self.shopId2 = self._url(goodsUrl)
        self.url1 = 'https://pas.suning.com/nsenitemsale_0000000%s_%s_5_999_100_025_0250199______1000173_.html?_=1571284185922&callback=wapData'%(self.shopId2,self.shopId)
        # self.url2 = 'https://pas.suning.com/nssnattache_%s_%s_9173_18_18_R1901001_20006_9173_0_5_0_000000010597840391_0_4588.00_999_0250199_025_3_0_0030000400CH9F0H1_0010132789___0021_000060021_30193816____157179760166147885_20002___.html?callback=attacheCommonLogic'%(self.shopId2,self.shopId)
        self.result = self._info()

    def _url(self, goodsUrl) -> (str,str):
        try:
            result = re.findall(r'com/product/(\d.+).html', goodsUrl)
            if not result:
                result = re.findall(r'suning.com/(\d.+).html', goodsUrl)
            result2 = result[0].split(r'/')
        except IndexError as e:
            raise IndexError('请检查 1 是否为苏宁易购商品链接，2 链接中需含有 product 字段。%s.'%e)
        print(result2)
        return result2[0],result2[1]

    def _info(self):
        try:
            r = requests.get(self.url1)
            result = r.text.strip()[8:-1]
            # if r'"code":"1"' in r.text:
            #     r2 = requests.get(self.url2)
            #     result = r2.text.strip()[19:-1]
        except requests.exceptions.RequestException as e:
            print('信息请求错误，请检查 id', e)
            return None
        # print(result)
        result = json.loads(result)
        return result

    def config(self):
        try:
            title = self.result['data']['data1']['data']['itemInfoVo']['itemDisplayName']
        except KeyError as e:
            print('标题名取值键值错误，请检查', e)
            return None            
        return title
    
    def price(self) -> float or None:
        try:
            price = self.result['data']['price']['saleInfo'][0]['promotionPrice']
        except KeyError as e:
            print('价格取值键值错误，请检查', e)
            return None            
        return float(price)
    def tPrice(self) -> float or None:
        """团购价"""
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