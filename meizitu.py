from pyquery import PyQuery as pq
import requests
import os
import multiprocessing
 
#请求每一页的链接获取组图链接
def get_url(i):
    url='http://www.meizitu.com/a/more_'+str(i)+'.html'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    html = requests.get(url=url, headers = headers).content.decode('gbk')
    doc = pq(html)  #请求到的链接初始化为pyquery类型
    lis = doc('#pagecontent .tit a').items()  #查找组图的链接，选择出 id=pagecontent标签 下 class=tit标签 中的a标签，再用.items()转换为可以遍历的对象
    for li in lis:  #遍历上面的结果，取出组图的链接和名字，名字只是为了后面保存的时候建文件夹
        url_g = li.attr('href')1
        name_g = li.text()
        if not os.path.exists('image1' + '/' + str(name_g)):  # 检测是否有image目录没有则创建
            os.makedirs('image1' + '/' + str(name_g))
        get_imgurl(name_g, url_g)  #调用获取组图内图片链接函数
    print('---------------下载完成------------------')
 
def get_imgurl(folder, imurl):  #获取组图内美张图片链接函数
    url = imurl
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    html = requests.get(url=url,headers=headers).content.decode('gbk')
    doc = pq(html)  #和上面那个函数一样，将请求到的链接初始化为pyquery类型
    lis = doc('#picture p img').items()  #获取 id=picture 下 p 标签 里的所有 img标签
    for li in lis:  #遍历，得到每张图的url和名字
        picname = li.attr('alt')
        picurl = li.attr('src')
        downloadimg(folder, picname, picurl)
 
def downloadimg(folder, name, url):  #下载保存图片
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    file = requests.get(url=url, headers=headers)
    filename = 'image1'+'/'+str(folder)+'/'+str(name)+'.jpg'
    fp = open(filename, 'wb')
    print(filename)
    fp.write(file.content)
    fp.close()
 
def main(i):
    get_url(i)
 
if __name__ == '__main__':
    page_star = input('请输入开始页：')
    page_over = input('请输入结束页：')
    group = [i for i in range(int(page_star), int(page_over) + 1)]
    print('开始为您下载第：' + str(group) + ' 页')
    pool = multiprocessing.Pool(processes=4)   #引入多进程，这里是4线程，可以自定义
    pool.map(main, group)