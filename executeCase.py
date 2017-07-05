__author__ = 'vip'
# coding=utf-8
import sys
import socket


reload(sys)
sys.setdefaultencoding("utf-8")
ADDRESS = ('172.16.230.180', 8888)
# ADDRESS = ('172.16.6.6', 8888)
reportFile = "C:\socketServer\socketClient"
connType = "execute"

"""
接收命令后执行
"""
def tryDo(sock):
    data = sock.recv(1024)
    args = data.split(" ")
    if args[0] == "Done":
        caseid = args[1]
        print 'Ready to do!'+caseid

"""
开始连接，每一次连接都执行这个方法，使服务器获取连接名称
"""
def startConn(sock):
    hostname = socket.gethostname()
    print hostname
    msg = "connName: "+hostname+"Type: "+connType
    sock.send(msg)
    res = sock.recv(1024)
    print res

"""
建立一个socket连接sock
与服务器开始通讯，服务器地址ADDRESS
1.当有文件新增或修改，上传文件到服务器
"""
if __name__ == '__main__':
    print u"服务器启动"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    startConn(sock)
    while 1:
        tryDo(sock)