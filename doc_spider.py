import os
import requests
#创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
 
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("创建新文件夹")
 
        print("创建成功")
    else:
        print("该文件夹已经存在")
 
host = 'https://view41.book118.com//img/?img='
url = 'https://view41.book118.com/pdf/GetNextPage'
 
pageNumber = 1
nextPageUrl = {}
thisPageUrl = '7o@o7xcocmmzkvwcNzdFX2WomykI7aFAfYKNVMTPPJYwVKlX2vVZCdL4Ws932iPT'
img_path = "D:/photo/book/"
mkdir(img_path)
for i in range(51):
    params = {
        'f': 'QzpcT2ZmaWNlV2ViMzY1XE9mZmljZVdlYlxjYWNoZVxQREZcMTE2MTIwNTExMjgyNzEzMzIwMjEwMTQ2NTlfODgwNjRcMzEyODExNi01ODQ0ZGVkYjE5NzdlLmRvYy50ZW1w',
        'img': thisPageUrl,
        'isMobile': 'false',
        'isNet': 'true',
        'readLimit': 't2lOjHovBX@TGrxHGTQHAg==',
        'furl': 'o4j9ZG7fK97PX9vZopx9OZEQwygFDDlsYeLf@VY1ztzuFpJRcU1Zd6761HH6tDx985563CmGkGRabmnThJuAJcF@F83GdTF5n4s3kivFThYdL9gWIQEAgQ=='
    }
    # 下载当前页放到D:/photo/book文件夹里面
    # title
    title = str(i + 1)
    web = requests.get(host + thisPageUrl)
    with open(img_path + title + ".png", "wb") as html:
        html.write(web.content)
    html.close()
 
    print('成功下载第%d页图片,链接%s' % (pageNumber, host + thisPageUrl))
    #动态获取下一页图片URL地址
    page = requests.get(url, params).json()
    nextPageUrl = page['NextPage']
    print(nextPageUrl)
 
    thisPageUrl = nextPageUrl
    pageNumber = pageNumber + 1