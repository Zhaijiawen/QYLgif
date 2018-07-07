# coding:utf-8
import urllib
import urllib.request
import re
import http.cookiejar
import time

# 目标对象正则表达式
rex = r'src="(http://www.qylbbs\d*.com/attachment/.*?\.gif)"'
# 目标url正则表达式
rexUrl = r'href="(http://www.qylbbs\d*.com/read/\d*)"'
# 目标名称
name = 1
# 目标网址
baseUrl = "http://www.qylbbs2.com/"
# headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}
# 获取cookie
request = urllib.request.Request(baseUrl, headers=headers)
cookieJar = http.cookiejar.CookieJar()
cookieProcess = urllib.request.HTTPCookieProcessor(cookieJar)

opener = urllib.request.build_opener(cookieProcess)
opener.open(request)

beginCount = input("起始页：")
endCount = input("结束页：")
try:
    beginCount = int(beginCount)
    endCount = int(endCount)
except:
    print("请输入数字！")
pageCount = range(beginCount, endCount)
for page in pageCount:
    pageUrl = baseUrl + "thread/81/%s&type=16" % page
    try:
        request = urllib.request.Request(pageUrl, headers=headers)
        opener = urllib.request.build_opener(cookieProcess)
        response = opener.open(request, timeout=10)

        htmlResult = response.read().decode('utf-8')
        urlResult = re.findall(rexUrl, htmlResult)
        urlList = list(urlResult)
    except:
        print(pageUrl + "访问出错")
    for url in urlList:
        try:
            request = urllib.request.Request(url, headers=headers)
            opener = urllib.request.build_opener(cookieProcess)
            response = opener.open(request, timeout=5)
            time.sleep(1)

            urlResult = response.read().decode('utf-8')
            gifList = re.findall(rex, urlResult)
        except:
            print(url + "访问出错")
            continue
        for gifUrl in gifList:
            try:
                urllib.request.urlretrieve(gifUrl, '.\pic\%s.gif' % name)
            except:
                print(gifUrl + "访问出错")
                continue
            name = name + 1
print("完成")
