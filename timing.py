# encoding:utf8
import time
import os
import re
import csv
from shop.jd import JD # 自定义
from shop.tm import TM
from shop.sn import SN
from shop.pdd import PDD
from apscheduler.schedulers.blocking import BlockingScheduler

basePath = os.path.dirname(os.path.abspath(__file__)) # 当前文件夹
log_path = os.path.join(basePath,'task.csv')

def get_date():
    """获取日期"""
    timestamp = int(time.time())
    time_local = time.localtime(timestamp) # #时间戳 转 时间数组
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local) # #时间数组 转 新的时间格式(2016-05-05 20:28:54)
    return dt

def get_url():
    with open(os.path.join(basePath, 'goods.txt'),'r',encoding='utf8') as f:
        good = f.readlines()
    url = None
    for i in good:
        if i != '\n':
            url = i.strip().replace(r'\n','')
            break
    if url:
        return url

def go(url):
    '''输入链接输出价格
    统一价格输出，以最低价格为标准，如有团购和单独购买以单独购买为准
    '''
    result = re.findall('://(.+?).com', url)
    if result:
        result = result[0]
        if 'yangkeduo' in result:
            pd = PDD(url)
            title,price = pd.main()
        elif 'suning' in result:
            sn = SN(url)
            title,price = sn.main()
        elif 'tmall' in result or 'taobao' in result:
            tm = TM(url) # 605030977928：联想笔记本 ； 603330883901 华为 mate30 pro ; 523962011119: 酸奶 
            title,price = tm.main()
        elif 'jd' in result:
            jd = JD(url) # 测试 id：100009083152 商品：联想 y9000x 笔记本电脑 2 热水壶 or 薯条？
            title,price = jd.main()
        else:
            raise TypeError('请检查输入的网站链接')
        print('标题 %s, 价格（多个价格以团购为准） %s. '%(title,price))
    else:
        raise TypeError('请检查输入是否为目标网站的商品详细页面链接')
    today = get_date() # 日期
    row = (today, title, price)
    with open(log_path,'a+',encoding='utf8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(row)


if __name__ == '__main__':
    url = get_url()

    # scheduler = BlockingScheduler()
    # scheduler.add_job(go,'cron', args=[url],hour='8-23', minute= '5,35' , second='15')
    # # scheduler.add_job(main,'cron', args=[3088512],hour='8-23', minute= 5 , second='15')
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass
    if url:
        go(url)
