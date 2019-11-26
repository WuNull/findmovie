# coding=utf-8
import urllib.request
import urllib.error
import re
opener = urllib.request.build_opener()#构建一个handler对象
def search():
    title = input("请输入电影名称:")
    title = title.encode('gb2312')
    req = urllib.request.Request('http://s.ygdy8.com/plus/so.php')
    #so.php请求参数将中文进行了Url.encode()，所以需要将中文encode('gb2312')处理
    req.data('kwtype=0&searchtype=title&keyword=%s' % title)
    html = opener.open(req).read().decode('gb2312')
    reg = r'/html/tv/oumeitv/[0-9]{8}/[0-9a-zA-Z.]{9,10}'
    return re.findall(reg, html)
search()
#/html/tv/oumeitv/20140930/46270.html
#/html/tv/oumeitv/20151007/49245.html
def openSearchResult():
    list = search()
    req = urllib.Request('http://www.ygdy8.com'+list[0])
    html = opener.open(req).read().decode('gb2312','ignore')
    reg = u'ftp://[a-z0-9]+:[a-z0-9]+@[a-z0-9]+.[a-z]{1,8}.[a-z]{3}:[\d]{4}/[\u4e00-\u9fa5]{0,10}[\W]*\[[\u4e00-\u9fa5]{0,10}www.[\w]{0,10}.[a-z]{3}\][\u4e00-\u9fa5]*[\d]+[\u4e00-\u9fa5]\[[\u4e00-\u9fa5]+\].rmvb'
    return re.findall(reg, html)
print(openSearchResult())
#ftp://dygod1:dygod1@y068.dydytt.net:1001/傲骨贤妻第六季/[阳光电影www.ygdy8.com]傲骨贤妻第六季第01集[中英双字].rmvb
#ftp://dygod2:dygod2@y009.dygod.org:1004/行尸走肉第五季/[阳光电影www.ygdy8.com]行尸走肉第五季第01集[中英双字].rmvb
#ftp://ygdy8:ygdy8@yg90.dydytt.net:2048/[阳光电影www.ygdy8.com]行尸走肉第八季第09集[中英双字].rmvb
#ftp://dygod1:dygod1@d315.dygod.org:5033/傲骨贤妻第三季/[电影天堂www.dy2018.net]傲骨贤妻第三季21集[中英双字].rmvb
#[\u4e00-\u9fa5]中文匹配
def getList():
    for i in openSearchResult():
        print(i)
getList()