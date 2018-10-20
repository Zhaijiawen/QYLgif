# coding:utf-8
import urllib
import urllib.request
import re
import http.cookiejar
import time
import threading
import os

# 目标对象正则表达式
rex = r'src="(http://www.\w*.com/attachment/.*?\.gif)"'
# 目标url正则表达式
rexUrl = r'href="(http://www.\w*.com/read/\d{6})"'

# 目标网址
# http://www.qbb0.com/
baseUrl = ""
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

# 判断目录
if(not os.path.exists(".\pic")):
    os.mkdir(".\pic")

def main():
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

        request = urllib.request.Request(pageUrl, headers=headers)
        opener = urllib.request.build_opener(cookieProcess)
        response = opener.open(request, timeout=10)

        htmlResult = response.read().decode('utf-8')
        urlResult = re.findall(rexUrl, htmlResult)
        urlList = list(set(urlResult))

        threads = [];
        for url in urlList:
            threads.append(threading.Thread(target=url_thread, args=(url,)));
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()


def url_thread(url):
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(cookieProcess)
    response = opener.open(request, timeout=5)
    time.sleep(1)

    urlResult = response.read().decode('utf-8')
    gifList = re.findall(rex, urlResult)
    # 目标名称
    name = 1
    for gifUrl in gifList:
        try:
            # 获取锁
            urllib.request.urlretrieve(gifUrl,
                                       '.\pic\%s.gif' % (threading.current_thread().getName() + "-" + str(name)))
            name = name + 1
        except:
            print(gifUrl)
            continue;


if __name__ == '__main__':
    main();
    print("完成!");
