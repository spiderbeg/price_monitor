import timing
"""
    1 调用 timing.py 中的 go 方法测试链接的可用性
    2 调用 timing.py 中的 go, get_url() 方法测试 goods.csv 文件中链接的可用性
"""

# 链接测试
# urls = ['https://m.suning.com/product/0000000000/000000011210599174.html?utm_source=baidu&utm_midium=brand-wuxian&utm_content=&utm_campaign=title&safp=f73ee1cf.wapindex7.113464229882.4&safc=prd.1.rec_14-40_0_A_ab:A',
# 'https://m.suning.com/product/0070067092/000000000188392234.html?utm_source=baidu&utm_midium=brand-wuxian&utm_content=&utm_campaign=title&safp=f73ee1cf.wapindex7.113464229882.60&safc=prd.1.rec_5-5_1018C,1014C$c3ae37eafeb814a098d120647449da6f_H_ab:A',
# 'https://m.suning.com/product/0000000000/000000000107426461.html?src=snsxpd_none_recssxcnxhq_1-3_p_0000000000_000000000107426461_rec_21-65_3_A&safp=f73ee1cf.71jyzx.112079032536.4&safc=prd.1.rec_21-65_3_A',
# 'https://m.suning.com/product/0000000000/10606656136.html?safp=f73ee1cf.phone2019.121927933306.2&safc=prd.0.0']

# 输入文本的链接可用性测试
if __name__ == '__main__':
    urls = timing.get_url()
    for url in urls:
        try:
            timing.go(url) # 获取返回信息 
        except BaseException as e:
            print(url,'\n',e)
