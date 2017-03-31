from error import *
def str_to_num(s,max_bits=32):
    try:
        num = int(s,10)
    except ValueError:
        try:
            num = int(s,2)
        except ValueError:
            try:
                num = int(s,16)
            except ValueError:
                raise NumberError(s)
    return origin_to_complement(num,max_bits)

def origin_to_complement(num,max_bits):
    if num < 0:
        num = (1 << max_bits) + num
    if num >= (1 << max_bits) or num < 0:
        raise NumberError(num)
    return num