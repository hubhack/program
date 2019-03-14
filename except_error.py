
'''try:
    fh = open ("testfile","w")
    fh.write("处理异常文件")
except IOError:
    print "Error:没有找到文件或读取文件失败"
else:
    print"内容写入文件成功"
    fh.close()

while True:

    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
'''
