import timing

urls = ['https://m.suning.com/product/0000000000/000000011210599174.html?utm_source=baidu&utm_midium=brand-wuxian&utm_content=&utm_campaign=title&safp=f73ee1cf.wapindex7.113464229882.4&safc=prd.1.rec_14-40_0_A_ab:A',
'https://m.suning.com/product/0070067092/000000000188392234.html?utm_source=baidu&utm_midium=brand-wuxian&utm_content=&utm_campaign=title&safp=f73ee1cf.wapindex7.113464229882.60&safc=prd.1.rec_5-5_1018C,1014C$c3ae37eafeb814a098d120647449da6f_H_ab:A',
'https://m.suning.com/product/0000000000/000000000107426461.html?src=snsxpd_none_recssxcnxhq_1-3_p_0000000000_000000000107426461_rec_21-65_3_A&safp=f73ee1cf.71jyzx.112079032536.4&safc=prd.1.rec_21-65_3_A',
'https://m.suning.com/product/0000000000/10606656136.html?safp=f73ee1cf.phone2019.121927933306.2&safc=prd.0.0']

for url in urls:
    mes = ['100','test',url]
    timing.go(mes)
