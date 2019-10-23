# encoding: utf8

from pyecharts import options as opts
from pyecharts.charts import Page, Line
import os
import csv

basePath = os.path.dirname(os.path.abspath(__file__)) # 当前文件夹

def line(title,checktime,price) -> Line:
    """绘图函数"""
    c = (
        Line()
        .add_xaxis(checktime)
        .add_yaxis(title, price, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="商品价格"),
                yaxis_opts=opts.AxisOpts(name="元/台"),
                xaxis_opts=opts.AxisOpts(name=title,
                    axislabel_opts=opts.LabelOpts(formatter="{value}", font_size=12, rotate=30,) # x,y 轴标签
                        )
                )
        )
    return c

def files():
    """
    输出字典，每一个键值为一张图表
    """
    global basePath
    files = {}
    with open(os.path.join(basePath,'goods.csv'),'r',encoding='utf8') as f:
        f_csv = csv.reader(f)
        next(f_csv) # 标题
        for row in f_csv: # 内容
            if row:
                replace_string = ['.',' ',r'/',r'\\'] # 特殊字符处理
                for rs in replace_string:
                    row[1] = row[1].replace(rs,'_')
                files.setdefault(row[0],[]).append(row[1])
    return files

def draw(files):
    """绘制图形文件"""
    datapath = os.path.join(basePath,'data')
    picpath = os.path.join(basePath,'pic')
    for k,i in files.items():
        page = Page()
        for n in i:
            with open(os.path.join(datapath, n +'.csv'),'r', encoding='utf8') as f:
                f_csv = csv.DictReader(f)
                price,checktime = [],[]
                for row in f_csv:
                    checktime.append(row['时间'])
                    price.append(row['价格'])
                title = n
            page.add(line(title,checktime,price)) # 24 发帖回帖变化图、近3月变化图、浏览、回复散点图
        page.render(os.path.join(picpath, k +'.html'))


if __name__ == '__main__':
    draw(files())