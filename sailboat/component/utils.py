import hashlib


def md5_encode(value):
    """ MD5 信息摘要"""
    h = hashlib.md5()
    h.update(value.encode("utf8"))
    res = h.hexdigest()
    return res