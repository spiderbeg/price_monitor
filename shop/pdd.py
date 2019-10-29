# encoding:utf8
import requests
import re
from bs4 import BeautifulSoup

class PDD:
    """
    功能：输入平多多商品链接，返回价格
    输入商品id，获取商品价格信息
    商品详细信息页：http://yangkeduo.com/goods.html?goods_id=6199937358
    """
    def __init__(self, goodsUrl):
        self.goodsId = self._url(goodsUrl)
        self.url = 'http://yangkeduo.com/goods.html?goods_id=%s'%self.goodsId
        self.headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
} 
        self.soup = self._info()
    
    def _url(self,goodsUrl):
        try:
            goodsId = re.findall(r'goods_id=(\d+)', goodsUrl)[0]
        except IndexError as e:
            raise IndexError('pdd -> _url 请检查 1 是否为拼多多商品链接，2 链接中需含有 goodss_id= 字段。%s.'%e)
        return goodsId

    def _info(self):
        """返回：商品信息的 BeautifulSoup 对象"""
        try:
            r = requests.get(self.url,headers=self.headers)
        except requests.exceptions.RequestException as e:
            print('pdd -> _info 商品详细页请求失败', e)
            return None
        soup = BeautifulSoup(r.text,features="lxml")
        # print(soup)
        return soup

    def title(self):
        """返回：商品标题"""
        try:
            title = self.soup.find(class_="_1pQOmeOt").text
        except AttributeError as e:
            print('pdd -> title 可能商品已下架标题 soup 属性错误，请检查', e)
            raise
        return title
    
    def price(self) -> float or None:
        """返回：商品价格
        未使用
        """
        try:
            price = self.soup.find(class_="_3r8Ds_Kf").text.replace('￥','').replace('单独购买','')
        except AttributeError as e:
            print('pdd -> price 单独购买 soup 属性错误，请检查', e)
            return None
        return float(price)

    def tPrice(self) -> float or None:
        """返回：商品团购价"""
        try:
            tprice = self.soup.find(class_="_3dlX1BNw").text.replace('￥','').replace('发起拼单','')
        except AttributeError as e:
            print('pdd -> tPrice 团购 soup 属性错误，请检查', e)
            return None
        return float(tprice)

    def main(self):
        title = self.title()
        tprice = self.tPrice()
        return title,tprice

if __name__ == "__main__":
    goodsurl = 'http://yangkeduo.com/goods.html?goods_id=40316089070&page_from=35&refer_page_name=index&refer_page_id=10002_1571389581170_8wbuwgxQex&refer_page_sn=10002'
    pd = PDD(goodsurl)
    title,price = pd.main()
    print('pdd -> __main__ 标题 %s, 团购 %s.'%(title,price))