# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:10:19 2018
@author: cy
"""
 
'''启动/调配爬虫'''
import requests
import json
from bs4 import BeautifulSoup as bs
import re
import time
 
XHR_HEAD_PATH = r'e:\lagou\xhr_head.txt'#获取xhr的HEAD
XHR_URL = r'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false' 
POS_HEAD_PATH = r'e:\lagou\pos_head.txt' #获取职位列表及职位信息的HEAD
PAGE_NUMBER = 29 #搜索得到的职位列表的页面
SAVE_PATH = r'e:\lagou\save.txt' #信息保存的的路径
 
#获取XHR
def get_xhr(head,num):
    data={'first':'true','kd':'数据挖掘','pn':num}
    re = requests.post(XHR_URL,headers = head, data = data)
    if re.status_code == 200:
        re_text = re.text
    else:
        re_text = None
        print('%d 页面访问错误'%num)
    return re_text
        
 
#解析xhr，获取positionID
def get_posID(xhr_text):
    if xhr_text == None:
        return None
    xhr_json = json.loads(xhr_text)
    result = xhr_json['content']['positionResult']['result']
    id_list = []
    for i in range(15):
        id_list.append(result[i]['positionId'])
    return id_list
 
#获取岗位信息html
def get_posInfo(id,head):
    if id == None:
        print('id为空')
        return None
   
    url = r'https://www.lagou.com/jobs/'+str(id)+'.html'
    print(url)
    re = requests.get(url,headers = head)
    if re.status_code != 200:
        return None
    pos_html = re.text
    return pos_html
            
            
 
#解析岗位信息
def analysis_pos(pos_html):
    if pos_html == None:
        print('岗位信息页面为空')
        return None
    soup = bs(pos_html)
    job_name = soup.find_all('span',class_='name')[0].text
   
    dd = soup.find_all('dd',class_='job_request')
    pattern = re.compile(r'>(.*?)</span>')
    result = pattern.findall(str(dd))
    for i in range(len(result)):
        result[i]  = result[i].replace('/','').strip()
        
    job_info = soup.find_all('dd',class_='job_bt')
    job_infos = str(job_info)
    return job_name, result, job_infos
    
 
 
def run():
    with open(XHR_HEAD_PATH,'r') as file:  #组装访问xhr的head
        xhr_text = file.read()
        xhr_sp = xhr_text.split('\n')
        xhr_head = {}
        n = len(xhr_sp)
        for i in range(n//2):
            xhr_head[xhr_sp[i*2].strip()] = xhr_sp[i*2+1].strip()
        print('xhr_head加载成功')
     
    with open(POS_HEAD_PATH,'r') as file:  #组装访问xhr的head
        pos_text = file.read()
        pos_sp = pos_text.split('\n')
        pos_head = {}
        n = len(pos_sp)
        for i in range(n//2):
            pos_head[pos_sp[i*2].strip()] = pos_sp[i*2+1].strip()
        print('pos_head加载成功')
    
    with open(SAVE_PATH,'w+',encoding='utf-8') as file:        
        for num in range(PAGE_NUMBER):
            xhr_json = get_xhr(xhr_head,num+1)  #获取xhr返回的json
            time.sleep(10)
            for i in posIDs:
                posInfoHtml = get_posInfo(i,pos_head)  #访问对应positionID的页面，获取html
                print('已访问%d页面'%i)
                job_name, result, job_info = analysis_pos(posInfoHtml) #对获取的HTML页面进行解析
                time.sleep(10)
                line = job_name+'0000'+str(result)+'0000'+job_info
                file.write(line+'\n')  
                print('页面%d已存储'%i)
 
if __name__ =='__main__':
    run()
    print('运行结束')
 
 