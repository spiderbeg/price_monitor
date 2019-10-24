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

# import logging
# formats = "%(asctime)s %(name)s %(levelname)s function:%(funcName)s -> :%(message)s"
# logging.basicConfig(format=formats, datefmt='%m/%d/%Y %I:%M:%S %p') # ,handlers=[logging.FileHandler(log_path, 'a+', 'utf-8')]
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.INFO)

basePath = os.path.dirname(os.path.abspath(__file__)) # 当前文件夹

def get_date():
    """获取日期"""
    timestamp = int(time.time())
    time_local = time.localtime(timestamp) # #时间戳 转 时间数组
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local) # #时间数组 转 新的时间格式(2016-05-05 20:28:54)
    return dt

def get_url():
    """读取商品链接
    返回：图像名，商品名，商品链接 元组
    """
    urls = []
    with open(os.path.join(basePath, 'goods.csv'),'r',encoding='utf8') as f:
        f_csv = csv.reader(f)
        next(f_csv) # 返回标题,直接到内容
        for row in f_csv: # 内容
            if row:
                urls.append(row)
    return urls

def go(url):
    '''输入：链接
    输出：(时间，标题，商品价格), 文件路径 元组
    统一价格输出，以最低价格为标准，如有团购和单独购买以单独购买为准
    '''
    result = re.findall('://(.+?).com', url[2])
    if result:
        result = result[0]
        if 'yangkeduo' in result:
            pd = PDD(url[2])
            title,price = pd.main()
        elif 'suning' in result:
            sn = SN(url[2])
            title,price = sn.main()
        elif 'tmall' in result or 'taobao' in result:
            tm = TM(url[2]) # 605030977928：联想笔记本 ； 603330883901 华为 mate30 pro ; 523962011119: 酸奶 
            title,price = tm.main()
        elif 'jd' in result:
            jd = JD(url[2]) # 测试 id：100009083152 商品：联想 y9000x 笔记本电脑 2 热水壶 or 薯条？
            title,price = jd.main()
        else:
            raise TypeError('请检查输入的网站链接')
        print('标题 %s, 价格（多个价格以团购为准） %s. '%(title,price))
    else:
        raise TypeError('请检查输入是否为目标网站的商品详细页面链接')
    # 文件名
    replace_string = ['.',' ',r'/',r'\\']
    for rs in replace_string:
        url[1] = url[1].replace(rs,'_')
    path = os.path.join(os.path.join(basePath, 'data'), url[1]+'.csv')

    today = get_date() # 日期
    return (today, title, price),path

def addData(row, path):
    """数据写入文件"""
    with open(path,'a+',encoding='utf8') as f:
        fieldnames = ['时间', '标题','价格']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0: # 如果内容为空则添加标题
            writer.writeheader()
        writer.writerow({'时间': row[0], '标题': row[1],'价格':row[2]})

def main():
    """运行程序"""
    urls = get_url()
    for url in urls:
        try:
            row,path = go(url) # 获取返回信息 
            addData(row,path) # 写入文件
        except:
            print('请求问题？')


if __name__ == '__main__':
    print('时间',get_date())
    main()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(go,'cron', args=[url],hour='8-23', minute= '5,35' , second='15')
    # # scheduler.add_job(main,'cron', args=[3088512],hour='8-23', minute= 5 , second='15')
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass
    
