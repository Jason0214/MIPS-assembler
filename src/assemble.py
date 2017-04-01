from error import *
from instruction_trans import *
from data_trans import *
import binascii

def asm_to_bytes(asm_file_path,output_file_pointer):
    asm_list,label_dict = pre_parse(asm_file_path)
    # init the instruction translater
    instruction_translater = InstructionTrans(label_dict)
    #constants
    _DATA_SEGMENT = 2
    _CODE_SEGMENT = 1
    _NONE = 0
    segment_type = _NONE
    segment_addr = 0
    current_addr = 0
    while len(asm_list) > 0:
        #line index of current instruction, used for error position
        line_index = asm_list[0][0]
        #real asm instruction
        asm_item = asm_list.pop(0)[1:]
        #specify the segment type
        if asm_item[0] in (".text",".data"): 
            if asm_item[0] == ".text":
                segment_type = _CODE_SEGMENT
            else:
                segment_type = _DATA_SEGMENT
            segment_addr = asm_item[1]
            if current_addr > segment_addr:
                raise SegmentCollision(line_index,segment_addr)
            # addresses between last segment and current segment all set to zero 
            for i in range(current_addr,segment_addr):
                output_file_pointer.write(b"\x00\x00\x00\x00")
            current_addr = segment_addr
        else:
            if segment_type == _CODE_SEGMENT:
                try:
                    result_in_int = instruction_translater.asm_to_bin(asm_item,current_addr)
                except TranslateError as e:
                    e.add_position_info(line_index)
                    raise e
                current_addr += 4
            else:
                result_in_int = asm_item[0]
                current_addr += 4
            output_file_pointer.write(int_to_bytes(result_in_int))

def int_to_bytes(result_in_int):
    hex_str = hex(result_in_int)[2:]
    while len(hex_str) < 8:
        hex_str = '0' + hex_str
    bytes_result = binascii.unhexlify(hex_str)
    return bytes_result


def asm_to_coe(asm_file_path,output_file_pointer):
    asm_list,label_dict = pre_parse(asm_file_path)
    instruction_translater = InstructionTrans(label_dict)
    #constants
    _DATA_SEGMENT = 2
    _CODE_SEGMENT = 1
    _NONE = 0
    segment_type = _NONE
    segment_addr = 0
    current_addr = 0    
    print("memory_initialization_radix=16;",file=output_file_pointer)
    print("memory_initialization_vector=",file=output_file_pointer)
    while len(asm_list) > 0:
        #line index of current instruction, used for error position
        line_index = asm_list[0][0]
        #real asm instruction
        asm_item = asm_list.pop(0)[1:]
        #specify the segment type
        if asm_item[0] in (".text",".data"): 
            if asm_item[0] == ".text":
                segment_type = _CODE_SEGMENT
            else:
                segment_type = _DATA_SEGMENT
            segment_addr = asm_item[1]
            if current_addr > segment_addr:
                raise SegmentCollision(line_index,segment_addr)
            # addresses between last segment and current segment all set to zero 
            for i in range(current_addr,segment_addr):
                print("00000000",end=",",file=output_file_pointer)
            current_addr = segment_addr
        else:
            if segment_type == _CODE_SEGMENT:
                try:
                    result_in_int = instruction_translater.asm_to_bin(asm_item,current_addr)
                except TranslateError as e:
                    e.add_position_info(line_index)
                    raise e
                current_addr += 4
            else:
                result_in_int = asm_item[0]
                current_addr += 4
            print(int_to_hex(result_in_int),end="",file=output_file_pointer)
            if len(asm_list) != 0:
                print(",",end="",file=output_file_pointer)
            else:
                print(";",end="",file=output_file_pointer)

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

def pre_parse(file_path):
    '''
        parse the pesudo instruction
        strip the comments in the assemble code
        split the assemble opcode and operand into tuple
        parse the data segment
        
        :param   file_path
        :return  (list,dict) 
    '''
    data_translater = DataTrans()
    assemble_container = []
    label_dict = {}
    #constants 
    _DATA_SEGMENT = 2
    _CODE_SEGMENT = 1
    _NONE = 0
    # variable point to the segment.instruction
    segment_type = _NONE
    current_addr = 0
    line_index = 0
    with open(file_path,"r") as fp:
        for line in fp.readlines():
            line_index += 1 #for easily display position of exception
            line_without_comments = strip_comments(line)
            #strip spaces in the head and tail of current line
            line_without_comments_space = line_without_comments.strip()
            #last line is not end with ";", combine the current one and last one
            if not line_without_comments_space:
                continue
            else: 
                # colon is the separate character between label and real code
                colon_index = line_without_comments_space.find(":")
                if colon_index != -1:
                    # split the line into label and assemble code
                    label = line_without_comments_space[:colon_index].strip()
                    try:
                        assemble_code = line_without_comments_space[colon_index+1:].strip()    #FIXME slice may raise a exception
                    except IndexError:
                        assemble_code = ""
                    if label in (".text",".data"):
                        # statement at the begining of a segment
                        current_addr = int(assemble_code,16)
                        if label == ".data":
                            segment_type = _DATA_SEGMENT
                        else:
                            segment_type = _CODE_SEGMENT
                        # still insert into container to be further read
                        # but instruction do not take memeory space
                        assemble_container.append((line_index,label,current_addr))
                        # next iteration
                        continue
                    else:
                        # label denotes the address of current instruction
                        # insert (label,address) as (key,value) into dict()
                        if label in label_dict:
                            raise DuplicateLabel(line,label)
                        label_dict[label] = current_addr
                else:
                    assemble_code = line_without_comments_space.strip()
                #check if assemble code is empty
                if assemble_code:
                    # insert assemble code to the container
                    # with every insertion, increase 'current_addr' 
                    # the size of the return list
                    if segment_type == _DATA_SEGMENT:
                        try:
                            list_of_data = data_translater.asm_to_bin(assemble_code)
                        except InvalidDataFormat as e:
                            e.add_position_info(line)
                            raise e
                        current_addr += len(list_of_data) * 4
                        for x in list_of_data:
                            assemble_container.append((line_index, x))
                    elif segment_type == _CODE_SEGMENT:
                        try:
                            list_of_tuple_inst = split_op(assemble_code,current_addr)
                        except PesudoInstFault as e:
                            e.add_position_info(line)
                            raise e
                        current_addr += len(list_of_tuple_inst) * 4
                        for inst_tuple in list_of_tuple_inst:
                            assemble_container.append((line_index,) + inst_tuple)
                    else:
                        raise SegmentNotSpecified(line,assemble_code)
    return assemble_container,label_dict

def strip_comments(line_of_inst):
    slash_index = line_of_inst.find("//")
    pound_index = line_of_inst.find("#")
    if slash_index == -1 and pound_index == -1:
        return line_of_inst
    elif slash_index == -1:
        return line_of_inst[:pound_index]
    elif pound_index == -1:
        return line_of_inst[:slash_index]
    elif pound_index < slash_index:
        return line_of_inst[:pound_index]
    else:
        return line_of_inst[:slash_index]
