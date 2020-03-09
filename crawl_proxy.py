# -*- coding: UTF-8 -*-
# 从快代理提取代理ip和端口，并验证连通性

import requests
import re
from lxml import etree
import time
import thread
from requests.adapters import HTTPAdapter
import threading
import sys
import random
import json

# proxies 格式
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}

# console colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NORM = '\033[2m'

# 提取数据
def getproxies(rcontent):
    selector = etree.HTML(rcontent)
    #print 'len', len(rcontent)
    # 提取 html 中的字符串
    content = selector.xpath('//html/body/div/div/div/div/div/table/tbody/tr')
    buff = ''
    dr = re.compile(r'<[^>]+>',re.S)
    proxieslist = []
    for item in content:
        # 提取<tbody>标签
        txt = etree.tostring(item,encoding="utf-8",method="html") 
        #print txt
        trs = etree.HTML(txt)
        parts = trs.xpath('//tr/td')
        # 提取每一个td
        #print parts
        #for part in parts[:2]:
        typeh = etree.tostring(parts[3],encoding="utf-8",method="html")
        iph = etree.tostring(parts[0],encoding="utf-8",method="html")
        porth = etree.tostring(parts[1],encoding="utf-8",method="html")
        ip = dr.sub('',iph).rstrip()
        port = dr.sub('',porth).rstrip()
        pt = dr.sub('',typeh).rstrip().lower()
        #print(pt,ip,port)
        proxieslist.append({'rank':0,'active':time.time(),'proxy':{pt:pt+'://'+ip+':'+port}})
    return proxieslist

def rankproxy(proxyset):
    proxy = proxyset['proxy']
    NETWORK_STATUS = True
    r=''
    s = requests.session()
    starttime = time.time()
    proxyset['active']=time.time()
    try:
        #print 'test proxy :', str(i)+'/'+str(len(rs))
        s.mount('http://', HTTPAdapter(max_retries=2))
        #r = requests.get("http://ipcheck.com", proxies=proxy,timeout=10)
        #validator=["http://ipcheck.com","http://ifconfig.me"]
        validator=["http://47.111.239.107/index.php"]
        r = requests.get(random.choice(validator), proxies=proxy,timeout=5)
    except requests.exceptions.ConnectTimeout:
        NETWORK_STATUS = False
    except requests.exceptions.ProxyError:
        NETWORK_STATUS = False
    except requests.exceptions.ChunkedEncodingError:
        NETWORK_STATUS = False
    except requests.exceptions.ReadTimeout:
        NETWORK_STATUS = False
    except requests.exceptions.TooManyRedirects:
        NETWORK_STATUS = False
    except requests.ConnectionError:
        NETWORK_STATUS = False
    except requests.RequestException:
        NETWORK_STATUS = False
    
    endtime = time.time()
    # get score
    mark = max(100.0 - (endtime-starttime), 0.0)

    # make rank
    rank = int(mark)
    s.close()
    # init set of rank
    proxyset['rank'] = -1
    # rank proxy
    if NETWORK_STATUS:
        if len(r.content) < 20:
            #print rank,proxy['http'],'\t->\t', r.content
            if r.content==re.findall(r'\d+\.\d+\.\d+\.\d+',proxy['http'])[0]:
                #print '+',rank,proxy['http'],'\t->\t', r.content
                #tested_proxies.append(proxy['http'])
                proxyset['rank'] = rank
    return proxyset
    

exitFlag = 0 
class CProxyRank (threading.Thread):   #继承父类threading.Thread
    def __init__(self, proxy, rqueue):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        self.proxy = proxy
        self.rqueue = rqueue
    def run(self):                 #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        # print "Starting " + self.name
        # print_time(self.name, self.counter, 5)
        # print "Exiting " + self.name
        self.rqueue.append(self)
        rankproxy(self.proxy)
        self.rqueue.pop(self.rqueue.index(self))

class CProxyPoolRank (threading.Thread):
    def __init__(self, pqueue=[],rqueue=[],proxypool=[]):
        threading.Thread.__init__(self)
        self.proxypool = proxypool
        self.pqueue = pqueue
        self.rqueue = rqueue
        self.killpoolranker=False
    def run(self):                 #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        self.pqueue.append(self)
        while not self.killpoolranker:
            ct = time.time()
            proxy_to_rank = []
            for proxy in self.proxypool:
                in_ranking = False
                for item in self.rqueue:
                    if item.proxy['proxy']['http'] == proxy['proxy']['http']:
                        in_ranking = True
                if (proxy['rank']>0 and (time.time() - proxy['active']) > 120 and not in_ranking) or (proxy['rank']==0 and not in_ranking):
                    proxy_to_rank.append(proxy)
            while len(self.rqueue) < 10 and len(proxy_to_rank)>0:
                ranker_thread = CProxyRank(proxy = proxy_to_rank.pop(), rqueue = self.rqueue)
                ranker_thread.start()
        self.pqueue.pop(self.pqueue.index(self))
    def killself(self):
        self.killpoolranker=True


# 从快代理下载代理数据，匿名和普通代理各抓9页
def processlinks():
    url = 'https://www.kuaidaili.com/free/inha/'
    url2 = 'https://www.kuaidaili.com/free/intr/'
    headers = {'user-agent': 'Mozilla'}
    proxies = []
    for i in range(1,15): 
        # print url+str(i)+'/'
        s = requests.session()
        s.mount('http://', HTTPAdapter(max_retries=2))
        r = requests.get(url+str(i)+'/', headers=headers)
        s.close()
        time.sleep(1.1)
        px = getproxies(r.content)
        # print px
        # print '-----------'
        proxies = proxies + px
        # r = s.get(url2+str(i), headers=headers)
        # time.sleep(1.1)
        # px = getproxies(r.content)
        # rs = rs+px
        #print len(proxies), 'proxies gets.'
    return proxies


class CProxyManage (threading.Thread):   #继承父类threading.Thread
    def __init__(self,lqueue=[],proxypool=[]):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        self.lqueue = lqueue
        self.proxies = proxypool
        self.kill = False
    def run(self):                 #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        self.lqueue.append(self)
        while not self.kill:
            #clean rank<1 proxy
            self.remove_failed()
            #get new proxies
            newproxies = processlinks()
            # combine proxies
            self.combine_proxies(newproxies, False)
            time.sleep(300)
        self.lqueue.pop(self.lqueue.index(self))
        self.kill = False
    def killself(self):
        self.kill=True
    def combine_proxies(self, newproxies=[], show=False):
        count = 0
        for item in newproxies:
            inlist = False
            for proxy in self.proxies:
                if item['proxy']['http']==proxy['proxy']['http']:
                    inlist = True
                    break
            if not inlist:
                self.proxies.append(item)
                count=count+1
        if show:
            print count,'proixes combined.'
    def remove_failed(self):
        proxy_to_remove=[]
        for proxy in self.proxies:
            if proxy['rank']<0:
                proxy_to_remove.append(proxy)
        for item in proxy_to_remove:
            self.proxies.remove(item)


class CProxyCrawl ():
    def __init__(self):
        self.rqueue = []
        self.lqueue = []
        self.pqueue = []
        self.proxypool = []
        self.proxymanager=CProxyManage(lqueue=self.lqueue, proxypool=self.proxypool)
        self.proxypoolranker = CProxyPoolRank(pqueue=self.pqueue, rqueue=self.rqueue, proxypool=self.proxypool)
    def runmanager(self):
        self.proxymanager.start()
    def runranker(self):
        self.proxypoolranker.start()
    def command(self):
        while True:
            s=raw_input(bcolors.ENDC+'cmd>')
            if s=='run manager':
                self.proxymanager.start()
            elif s=='run ranker':
                self.proxypoolranker.start()
            elif s=='stop ranker':
                self.proxypoolranker.killself()
            elif s=='stop manager':
                self.proxymanager.killself()
            elif s=='list':
                olist = self.proxypool[:]
                for proxy in olist:
                    print bcolors.ENDC+'rank:',bcolors.HEADER+str(proxy['rank']),bcolors.ENDC+'url:',bcolors.WARNING+proxy['proxy']['http'],bcolors.OKGREEN+str(round(time.time()-proxy['active']))+bcolors.ENDC+'\'s before'
            elif s=='list fine':
                olist = self.proxypool[:]
                for proxy in olist:
                    if proxy['rank']>0:
                        print bcolors.ENDC+'rank:',bcolors.HEADER+str(proxy['rank']),bcolors.ENDC+'url:',bcolors.WARNING+proxy['proxy']['http'],bcolors.OKGREEN+str(round(time.time()-proxy['active']))+bcolors.ENDC+'\'s before'
            elif s=='show ranking':
                for item in self.rqueue:
                    proxy = item.proxy
                    print 'ranking:',proxy['proxy']['http']
            elif s=='remove failed':
                self.proxymanager.remove_failed()
            elif s=='save list':
                ll = self.proxypool[:]
                ss = json.dumps(ll)
                f=open('list.json','w')
                f.write(ss)
                f.close()
                print 'proxypool ',len(ll),'proxies saved.'
            elif s=='load list':
                f=open('list.json','r')
                ss=f.read()
                f.close()
                dd = json.loads(ss)
                self.proxymanager.combine_proxies(dd, True)
            elif s=='status':
                print 'manager:',len(self.lqueue)
                print 'poolworker:',len(self.pqueue)
                print 'ranker:',len(self.rqueue)
            elif s=='quit':
                self.proxymanager.killself()
                self.proxypoolranker.killself()
                print 'quitting...'
                break
            elif s=='\n' or s=='':
                pass
            else:
                print 'unknown cmd'

# 多线程测试代理的连通性
#
# 如果指定了文件，保存代理服务器到文件
# if len(sys.argv) == 2:
#     f = open(sys.argv[1],'w')
#     f.write('\r\n'.join(tested_proxies))
#     f.close()
#     print 'proxy list write to ',sys.argv[1] 

if __name__ == "__main__":
    proxycrawler = CProxyCrawl()
    proxycrawler.command()