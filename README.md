# 商品价格监控
## 实现功能
* 输入天猫、苏宁、京东、拼多多（网页页面<http://yangkeduo.com/>）任一商品链接，不是口令。**请复制选择好商品配置的页面链接**，即返回相应商品价格，并保存到文件。商品页面若有团购与单独购买两个价格，返回团购价格。
* 使用 Windows 任务计划或 Linux 定时任务，定时执行程序。获取不同时段的商品价格信息。目前支持一个定时任务查询一件商品。
* 单独运行画图程序，可根据定时任务获取的数据，生成商品价格时间变化折线图。
## 快速上手
1. 在 goods.txt 中输入需要查询的商品链接。
2. 使用 Windows 任务计划或 Linux 定时任务，定时执行程序 **timing.py**。
3. 获取到数据后，运行 **draw.py** 即会生成含有商品价格时间变化折线图的**price.html**。
## 定时任务详解
### Windows 任务计划
* 推荐阅读<https://mp.weixin.qq.com/s/JKFvnmtlEqaE8GxbX6Fpyw>
* 注意如果你的 Python 使用的是虚拟环境，那么请找到你虚拟环境的 pythonw.exe(注意这里 python.exe 与pythonw.exe 都可以使用，使用 pythonw.exe 是为了避免控制台一闪而逝的现象，不必纠结).
### Linux crontab 定时任务
* 推荐阅读 <https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html>
* 两个执行示例

      15 8 * * * myCommand # 每天上午8点15分执行
      15 8-23 * * * myCommand # 每天8点到晚上23点，每个小时第15分钟执行 
 
## 项目思路
### 部分问题回答
* 项目的大致思路流程：第一步：使用**商品详细页链接**获取商品信息与商品**价格**，并保存获取数据 **时间、商品介绍，价格** 到 csv 文件中；第二步：使用定时任务**定时执行**第一步完成的程序；第三步：读取前两步获取到的时间、商品介绍、价格。使用 **pyecharts** 绘制绘制商品价格时间变化折线图。
* 为什么不适用 pc 端来调试网页，获取价格信息？ 因为在未登录状态天猫的详细商品页的信息是虚假的，同时从移动端网页入手，可以降低调试难度。
* 谷歌浏览器如何开启手机调试模式？ F12 进入开发者模式，然后鼠标点击一下，具体见下图。
* 
### 商品详细页源代码中获取价格
* 这里以链接商品 <https://item.m.jd.com/product/100009082500.html> 介绍过程。相关代码位于**shop**文件夹下 **jd.py** 中。 在谷歌浏览器手机调试模式下输入链接。然后输入页面价格查找价格文件所处位置。发现价格在原网页中。那么接下来就是，使用提取价格信息了。代码如下：

        import requests
        from bs4 import BeautifulSoup
        
        r = requests.get('https://item.m.jd.com/product/100009082500.html')
        soup = BeautifulSoup(r.text, features="lxml")
        result = soup.find(class_="price large_size")
        price = result.text.strip().replace('¥','') # 获取价格
        
### 从接口获取商品信息
* 示例链接 <https://m.suning.com/product/0070074466/646336020.html>. 相关代码位于 **shop** 文件夹下 **sn.py** 中。重复上一步操作，发现源网页代码中不存在价格信息，那么就接着找其它请求中的信息。找到后发现是个接口，那接下来就是获取数据了。

      # url = 'https://m.suning.com/product/0070074466/646336020.html' 商品详细页，里面的两个id是我们所需要的。
      # 我们发现的数据接口
      url = 'https://pas.suning.com/nsenitemsale_0000000646336020_0070074466_5_999_100_025_0250199______1000173_.html?_=1571284185922&callback=wapData'
      r = requests.get(url)
      result = r.text.strip()[8:-1]
      result = json.loads(result)
      price = result['data']['price']['saleInfo'][0]['promotionPrice']
