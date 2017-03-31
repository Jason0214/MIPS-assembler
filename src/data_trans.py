from error import *
from number_trans import *

class DataTrans():
    def __init__(self):
        pass
    def asm_to_bin(self,line_of_data_and_inst):
        '''
            check the pesudo instruction, if exists,
            parse it. Push every 32bits-wide data into 
            the list and return it.

            :return [int,...]
        '''
        ret_list = []
        inner_space_index = line_of_data_and_inst.find(" ")
        pesudo_inst = line_of_data_and_inst[:inner_space_index].lower()
        line_of_data = line_of_data_and_inst[inner_space_index+1:].strip()
        if pesudo_inst in (".dword",".word",".byte"):
            # can not just split with comma, since comma may be wrapped inside a pair of 
            # quotes, so we do it naively.   A VERY TRICKY MISTAKE MAYBE MADE
            encounter_double_quote = False
            encounter_single_quote = False
            data_list = []
            temp_string = ""
            for ch in line_of_data:
                if ch == "," and (not encounter_double_quote) and (not encounter_single_quote):
                    data_list.append(temp_string)
                    temp_string = ""    
                else:
                    if ch == "'":
                        encounter_single_quote = not encounter_single_quote
                    if ch == '"':
                        encounter_double_quote = not encounter_double_quote
                    temp_string += ch
            data_list.append(temp_string)
            # select different types of data
            if pesudo_inst == ".dword":
                ret_list = self.dd_data_trans(data_list)
            elif pesudo_inst == ".word":
                ret_list = self.dw_data_trans(data_list)
            elif  pesudo_inst == ".byte":
                ret_list = self.db_data_trans(data_list)
        elif pesudo_inst in ("resb","resw","resd"):
            size = str_to_num(line_of_data)
            if pesudo_inst == "resd": 
                for i in range(0,size):
                    ret_list.append(0)
            elif pesudo_inst == "resw":
                for i in range(0,size//2+1):
                    ret_list.append(0)
            else:
                for i in range(0,size//4+1):
                    ret_list.append(0)
        else:
            data_list = list(map(lambda x: x.strip(), line_of_data.split(",")))
            ret_list = self.dd_data_trans(data_list)
        return ret_list

    def dd_data_trans(self,raw_data_list):
        '''
            :param  [string,]
            :return [int,]
        '''
        dd_list = []
        for x in raw_data_list:
            if x[0] in ("'",'"') and x[0] == x[-1]:
                index = 0
                s = x[1:-1]
                while index + 3 < len(s):
                    dd_list.append((ord(s[index])<<24) + (ord(s[index+1])<<16) + ((ord(s[index+2]))<<8) + ord(s[index+3]))             
                    index += 4
                remain = len(s) - index
                # use 0 fill in remain bytes
                if remain > 0:
                    j = 0
                    temp = 0
                    while j < remain:
                        temp = temp << 8 + ord(s[index])
                        index += 1
                    temp << ((4-remain) * 8)
                    dd_list.append(temp)
            elif x[:2] == "0x":
                if len(x) != 10:
                    raise InvalidDataFormat(x)
                # little-endian
                value_in_st = x[:2] + x[2:][::-1]                
                try:
                    dd_list.append(int(value_in_st,16))
                except ValueError:
                    raise InvalidDataFormat(x)
            else:
                raise InvalidDataFormat(x)
        return self._merge(dd_list,1)

    def dw_data_trans(self,raw_data_list):
        '''
            :param  [string,]
            :return [int,]
        '''
        dw_list = []
        for x in raw_data_list:
            if x[0] in ("'",'"') and x[0] == x[-1]:
                index = 0
                s = x[1:-1]
                while index + 1 < len(s):
                    dw_list.append((ord(s[index])<<8) + ord(s[index+1]))
                    index += 2
                remain = len(s) - index
                if remain > 0:
                    dw_list.append(ord(s[index])<<8)
            elif x[:2] == "0x":
                if len(x) != 6:
                    raise InvalidDataFormat(x)
                # little-endian
                value_in_st = x[:2] + x[4:] + x[2:4]
                try:
                    dw_list.append(int(value_in_st,16))
                except ValueError:
                    raise InvalidDataFormat(x)
            else:
                raise InvalidDataFormat(x)
        return self._merge(dw_list,2)

    def db_data_trans(self,raw_data_list):
        '''
            :param  [string,]
            :return [int,]
        '''
        db_list = []
        for x in raw_data_list:
            if x[0] in ("'",'"') and x[0] == x[-1]:
                s = x[1:-1]
                for bytes_ in s:
                    db_list.append(ord(s[index]))
            elif x[:2] == "0x":
                if len(value_in_st) != 4:
                    raise InvalidDataFormat(x)
                # little-endian
                value_in_st = x
                try:
                    db_list.append(value_in_st)
                except ValueError:
                    raise InvalidDataFormat(x)
            else:
                raise InvalidDataFormat(x)
        return self._merge(db_list,4)

    def _merge(self,list_to_merge,step):
        '''
            :param [int,],int
            :return [int,]

            the value of 'step' can only be among (1,2,4)
        '''
        dd_bytes_list = []
        if step == 1:
            return list_to_merge
        elif step == 2:
            index = 0
            while index + 1 < len(list_to_merge):
                dd_bytes_list.append((list_to_merge[index] << 16) +list_to_merge[index+1])
                index += 2
            remain = len(list_to_merge) - index
            if remain == 1:
                dd_bytes_list.append(list_to_merge[index] << 16)
        elif step == 4:
            index = 0
            while index + 3 < len(list_to_merge):
                dd_bytes_list.append((list_to_merge[index] << 24) + (list_to_merge[index+1] << 16) + (list_to_merge[index+2] << 8) + list_to_merge[index+3])
                index += 4
            remain = len(list_to_merge) - index
            if remain == 3:    
                dd_bytes_list.append((list_to_merge[index] << 24) + (list_to_merge[index+1] << 16) + (list_to_merge[index+2] << 8))
            elif remain == 2:
                dd_bytes_list.append((list_to_merge[index] << 24) + (list_to_merge[index+1] << 16))
            elif remain == 1:
                dd_bytes_list.append(list_to_merge[index] << 24)
            else: #remain == 0
                pass
        return dd_bytes_list

if __name__ == "__main__":
    data_translater = DataTrans()
    data_string = input("input a line of MIPS assemble data: ")
    try:
        data_in_list = data_translater.asm_to_bin(data_string)
    except Error as e: 
           print(e.info)
           print(e.bug)
           raise e
    for x in data_in_list:
        binary_string = bin(x)[2:]
        while len(binary_string) < 32:
            binary_string = "0" + binary_string
        print(binary_string)