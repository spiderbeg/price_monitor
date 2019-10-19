# encoding: utf8

from pyecharts import options as opts
from pyecharts.charts import Page, Line
import os
import csv

basePath = os.path.dirname(os.path.abspath(__file__)) # 当前文件夹

def line() -> Line:
    global basePath
    # csv 文件读取
    with open(os.path.join(basePath,'task.csv'),'r',encoding='utf8') as f:
        f_csv = csv.DictReader(f)
        price,checktime = [],[]
        for row in f_csv:
            checktime.append(row['time'])
            price.append(row['price'])
        title = row['title']
        
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
if __name__ == '__main__':
    line().render(os.path.join(basePath,'price.html'))