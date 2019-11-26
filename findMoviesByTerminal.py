"""
python-version: 3.8.0
查找电影 小工具
实现思路:
1.实现电影资源网站的搜索功能
2.获取搜索结果的网页信息
3.进入电影详情页面获取播放和下载地址
"""
# coding=utf-8
import requests
from lxml import etree
from time import time

# 请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

# 搜索功能入口
def index_page(title):
    # 输入编码格式为utf-8
    # 设置 请求头参数
    data = {
        "submit": "search",
        "wd": title
    }
    url = "http://www.209zy.com/index.php?m=vod-search"
    response = requests.post(url=url, data=data, headers=headers)
    return response.text

# 搜索页面html分析
def parse_page(content):
    tree = etree.HTML(content)
    # 电影名称
    movie_name = tree.xpath('//div[@class="xing_vb"]/ul/li/span[@class="xing_vb4"]/a/text()')
    # 电影详情url
    movie_url = tree.xpath('//div[@class="xing_vb"]/ul/li/span[@class="xing_vb4"]/a/@href')
    # 公共url
    public_url = "http://www.209zy.com/index.php"
    # string 转 list, 添加url前缀
    movie_url = list(map(str, movie_url))
    movie_url_list = []
    for i in movie_url:
        temp_url = public_url + i
        movie_url_list.append(temp_url)
    # 返回对象(movie_name电影名称,movie_url电影地址)
    positions = {
        "movie_name": movie_name,
        "movie_url": movie_url_list
    }
    return positions

# 详情页面入口
def detail_page(positions):
    # 获得影片链接
    movie_url_list = positions.get('movie_url')
    # 定义一个空数组 存储 电影名称和播放地址和下载地址 对象
    list_movie = []
    for i in movie_url_list:
        response = requests.get(url=i, headers=headers)
        movie = parse_detail_page(response.text)
        list_movie.append(movie)
    return list_movie

# 详情页面分析
def parse_detail_page(detailPage):
    tree = etree.HTML(detailPage)
    # 电影名称 和 清晰程度
    movie_name = tree.xpath('//div[@class="vodh"]/h2/text()') + tree.xpath('//div[@class="vodh"]/span/text()')
    # 电影观看url 和 下载url
    movie_url = tree.xpath('//div[@class="vodplayinfo"]/div/ul/li/input[@name="copy_sel"]/@value')
    # string 转数组 list
    movie_url = list(map(str, movie_url))
    # 截取电影观看地址
    movie_url_watch = movie_url[0]
    # 截取电影下载地址
    movie_url_download = movie_url[1]
    movie = {
        "movie_name": movie_name,
        "movie_url_watch": movie_url_watch,
        "movie_url_download": movie_url_download

    }
    return movie

# main函数
if __name__ == '__main__':
    print('开始查找电影...')
    # 开始时间
    start = time()
    title = input("请输入电影名称:")
    # 获取页面内容
    content = index_page(title)
    # 搜索页面信息
    positions = parse_page(content)
    # 获取movie集合信息
    movie_list = detail_page(positions)
    print(movie_list)
    # 结束时间
    end = time()
    print('总共耗费了%.3f秒' % (end - start))
    print('电影查询完毕！')