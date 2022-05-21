import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

def obscure(data):
    return b64e(zlib.compress(data, 9))

def unobscure(obscured):
    return zlib.decompress(b64d(obscured))