# coding=utf-8
import socket
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
ADDRESS = ('172.16.230.189', 8888)
connType = "done"

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
从服务器返回连接列表
"""
def getConnList(sock):
    print 'getList'
    time.sleep(2)
    sock.send('getList')
    res = sock.recv(1024)
    print str(res)

"""
指定agent执行操作
"""
def done(sock, connName, casetype, id ,name ):
    print u"指定执行"
    sock.send('done ' + ' ' + connName + ' ' + casetype + ' ' + id + ' ' + name)

"""
命令server指定client执行
"""
def getlist():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    startConn(sock)
    getConnList(sock)
    sock.close()

def runTest(conn, casetype, caseName,name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    startConn(sock)
    done(sock, conn, casetype, caseName , name)
    sock.close()

# getlist()
# runTest('172.16.6.6', '中文')
