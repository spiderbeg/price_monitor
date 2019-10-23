# encoding:utf8
import requests
import json
import re
from urllib.parse import quote

class TM:
    """
    功能：在商品详细页显示商品已选的条件下。输入商品链接，获取天猫商品价格 
    商品详细页：https://detail.m.tmall.com/item.htm?id=605030977928&skuId=4241317581009
    商品价格及配置信息;https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22605030977928%22%7D
    # data={"itemNumId":"605030977928"}
    """
    def __init__(self, goodsUrl):
        """shopId: 单一商品中代表单一商品，商品有配置分类时，则代表一类商品，sku 代表某一具体商品。"""
        self.shopId,self.sku = self._url(goodsUrl)
        self.data = self._getData()
        self.url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%s'%self.data
        self.headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
}
        self.result,self.resultn = self._info() # self.result 取名字使用，self.resultn 取价格使用

    def _url(self,goodsUrl):
        """从输入链接中获取能确定商品的 id
        输入：商品链接；
        返回：商品 id 元组
        """
        try:
            gid = re.findall(r'id=(\d+)', goodsUrl)[0]
            sku = re.findall(r'skuId=(\d+)', goodsUrl) # 电脑手机选中后会生成 skuid
        except IndexError as e:
            raise IndexError('请检查 1 是否为天猫商品链接，2 链接中需含有 id(必需),sku(非必需) 字段。%s.'%e)
        if sku:
            sku = sku[0]
        else:
            sku = None
        print(gid,sku)
        return gid,sku

    def _getData(self):
        data = quote('{"itemNumId":"%s"}'%self.shopId)
        return data

    def _info(self):
        """返回：商品信息 json 数据元组，在生成实例时完成"""
        try:
            r = requests.get(self.url,headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('获取商品信息请求出错',e)
            raise ValueError('商品信息接口请求错误请检查详细信息')
        result = r.json()['data']
        resultn = json.loads(r.json()['data']['apiStack'][0]['value'])
        return result,resultn

    def config(self):
        """返回：商品信息标题"""
        try:
            result2 = self.result['apiStack'][0]['value']
            result2 = json.loads(result2)
            name = result2['item']['title']
        except KeyError as e:
            print('该商品应为淘宝商品，非天猫商品 %s'%e)
            name = self.result['item']['title']
        return name
    
    def subPrice(self):
        """返回：预售商品价格，如 y9000x"""
        try:
            price = self.resultn['price']['subPrice']['priceText']
            if not price.isdigit():
                raise TypeError('请确定是否为选择好配置的商品，或检查商品链接中是否含有 skuid')
            return float(price)
        except KeyError as e:
            print('字典取值错误, 请检查此商品是否为预售商品', e)
            return None

    def sPrice(self) -> float or None:
        """返回：单一商品，单一价格"""
        try:
            price = self.resultn['price']['price']['priceText']
            return float(price)
        except KeyError as e:
            print('字典取值错误，请检查此商品是否为只有一个价格的单一商品', e)
            return None

    def mPrice(self) -> float or None:
        """可选配置商品,需 sku
        sku: 代表某一具体商品
        """
        try:
            temp = self.resultn['skuCore']['sku2info']
            price = temp[self.sku]['price']['priceText']
        except KeyError as e:
            print('字典取值错误，请检查此商品是否为可选配置商品, 请提交选中配置后的商品链接', e)
            return None
        return float(price)
        

    def main(self):
        """查询价格
        """
        title = self.config()
        price = self.subPrice()
        if not price:
            if self.sku:
                price = self.mPrice()
            else:
                price = self.sPrice()
        return title,price

if __name__ == '__main__':
    goodsurl = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.4.5c9a2a683BItCM&id=558420556696&skuId=4387878194208&user_id=1917047079&cat_id=2&is_b=1&rn=00bb62d66e745f2057c1eff097f36ade'
    tm = TM(goodsurl) # 605030977928：联想笔记本 ； 603330883901 华为 mate30 pro ; 523962011119: 酸奶 
    title,price = tm.main()
    print('标题 %s; 价格 %s.'%(title,price))
        