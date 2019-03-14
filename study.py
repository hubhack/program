import os
import requests
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print('创建文件夹')
        print('创建成功')
    else:
        print('该文件已经存在')
        