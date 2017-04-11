from error import *
import binascii

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

def complement_to_origin(num,max_bits):
    if num > (1 << max_bits):
        raise NumberError(num)
    if num < (1 << (max_bits-1)): # positive
        return num
    else: #negative
        return num - (1 << max_bits)


def int_to_binary(result_in_int):
    bin_str = bin(result_in_int)[2:]
    while len(bin_str) < 32:
        bin_str = '0' + bin_str
    return bin_str
    
def int_to_hex(result_in_int):
    hex_str = hex(result_in_int)[2:]
    while len(hex_str) < 8:
        hex_str = "0" + hex_str
    return hex_str

def int_to_bytes(result_in_int):
    hex_str = hex(result_in_int)[2:]
    while len(hex_str) < 8:
        hex_str = '0' + hex_str
    bytes_result = binascii.unhexlify(hex_str)
    return bytes_result

if __name__ =="__main__":
    print(str_to_num("-4",16))
