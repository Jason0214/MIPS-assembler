from number_trans import *
from error import *


def split_op(line_of_instruction,addr_of_instruction = 0):
    '''
        translate pesudo instruction into real MIPS instruction

        :return [(opcode_32bits),(opcode_32bits),(opcode_32bits) ...]
    '''
    #find index of the space separating the operation and operands
    inner_space_index = line_of_instruction.find(" ")
    #split the instruction to opcodes and operands
    #type(operation) = string
    #type(operands) = list
    if inner_space_index != -1:
        operation = line_of_instruction[:inner_space_index].lower()
        operands = list(map(lambda x: x.strip(),line_of_instruction[inner_space_index+1:].split(",")))
    else:
        operation = line_of_instruction.lower()
        operands = []
    # the following code translate pesudo instruction into real instruction
    if operation == "la":
        if len(operands) == 2 and operands[1] == "address":
            return [("addiu",operands[0],"$zero",str(addr_of_instruction >> 16)),
                    ("sll",operands[0],operands[0],"16"),
                    ("addiu",operands[0],operands[0],str(addr_of_instruction & 0x00ff))]
        else:
            raise InvalidPesudoInst(line_of_instruction)
    elif operation == "move":
        if len(operands) == 2:
            return [("add",operands[0],operands[1],"$zero")]
        else:
            raise InvalidPesudoInst(line_of_instruction)
    elif operation == "li":
        if len(operands) == 2:
            try:
                imme_num = str_to_num(operands[1],32)
            except NumberError as e:
                raise InvalidPesudoInst(line_of_instruction)
            return [("addiu",operands[0],"$zero",str(imme_num >> 16)),
                    ("sll",operands[0],operands[0],"16"),
                    ("addiu",operands[0],operands[0],str(addr_of_instruction & 0x00ff))]
        else: 
            raise InvalidPesudoInst(line_of_instruction)
    else:
        return [(operation,)+tuple(operands)]


class InstructionTrans():
    def __init__(self,label_dict = dict()):
        self._symbol_table = label_dict
        self._R_TYPE_DICT = {"add":0x20,"addu":0x21,"sub":0x22,"subu":0x23,"and":0x24,"or":0x25,"xor":0x26,"nor":0x27,"jr":0x8,"jalr":0x9,
                            "sllv":0x04,"srlv":0x06, "srav":0x07,"slt":0x2a,"sltu":0x21,"sll":0x00,"srl":0x02,"sra":0x03}
        self._I_TYPE_DICT = {"addi":0x8,"addiu":0x9,"ori":0xd,"andi":0xc,"xori":0xe,"lui":0xf,"slti":0xa,"sltiu":0xb,"lw":0x23,"lb":0x20,"lbu":0x24,"lh":0x21,"lhu":0x25,
                            "sw":0x2b,"sh":0x29,"sb":0x28,"beq":0x4,"bne":0x5,"bgtz":0x7,"blez":0x6,}#"bltz":,"bltzal","bgez":,"bgezal",}
        self._J_TYPE_DICT = {"jal":0x03,"j":0x02}
        self._SYS_DICT = {"syscall":0x0c,"break":0x0d}
        self._REG_DICT = {"zero":0,"at":1,"v0":2,"v1":3,"a0":4,"a1":5,"a2":6,"a3":7,"t0":8,"t1":9,"t2":10,"t3":11,"t4":12,"t5":13,"t6":14,"t7":15,
                        "s0":16,"s1":17,"s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,"t8":24,"t9":25,"k0":26,"k1":27,"gp":28,"sp":29,"fp":30,"ra":31}
    
    def asm_to_bin(self,instruction,current_addr = 0):
        '''
        get a tuple of operation and operands
        return result in the form of integer
        '''
        operation = instruction[0]
        operands = instruction[1:]
        try:
            if operation in self._R_TYPE_DICT:
                return self._r_type_asm_to_bin(operation,operands)
            elif operation in self._I_TYPE_DICT:
                return self._i_type_asm_to_bin(operation,operands,current_addr)
            elif operation in self._J_TYPE_DICT:
                return self._j_type_asm_to_bin(operation,operands)
            else:
                raise InvalidInstruction(operation)
        except TranslateError as e:
            raise e

    def _r_type_asm_to_bin(self,operation,operands):
        opcode = 0b00000
        func = self._R_TYPE_DICT[operation]
        if func in (0x00,0x02,0x03): #shift
            if len(operands) == 3:
                rs = 0b00000
                rd = self._reg_trans(operands[0])
                rt = self._reg_trans(operands[1])
                shamt = str_to_num(operands[2], 5)
            elif len(operands) < 3:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        elif func in (0x8,0x9): #jr
            if len(operands) == 1:
                rd = 0b00000
                rs = self._reg_trans(operands[0])
                rt = 0b00000
                shamt = 0b00000
            elif len(operands) < 1:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        else:
            if len(operands) == 3:
                shamt = 0b00000
                rd = self._reg_trans(operands[0])
                rs = self._reg_trans(operands[1])
                rt = self._reg_trans(operands[2])
            elif len(operands) < 3:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        return (opcode<<26) + (rs<<21) + (rt<<16) + (rd<<11) + (shamt<<6) + func


    def _i_type_asm_to_bin(self,operation,operands,current_addr):
        '''
            :param int,[string,]
            :return b''
        '''
        opcode = self._I_TYPE_DICT[operation]
        if opcode in (0x23,0x20,0x24,0x21,0x25,0x2B,0x28,0x29):#sw lw etc.
            if len(operands) == 2:
                rt = self._reg_trans(operands[0])
                front_bracket = operands[1].find("(")
                back_bracket = operands[1].find(")")
                if back_bracket != -1 and front_bracket != -1 and front_bracket < back_bracket:
                    imme = int(operands[1][:front_bracket],10)
                    rs = self._reg_trans(operands[1][front_bracket+1:back_bracket])
                else:
                    raise InvalidInstruction(operands[1])
            elif len(operands) < 2:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        elif opcode in (0x4,0x5):  #beq bne
            if len(operands) == 3:
                if operands[2] in self._symbol_table:
                    imme = origin_to_complement((self._symbol_table[operands[2]] - current_addr - 4)>>2,16)
                else:
                    try:
                        imme = origin_to_complement(int(operands[2],16)>>2,16)
                    except (ValueError,NumberError):
                        raise InvalidLabel(operands[2])
                rs = self._reg_trans(operands[0])
                rt = self._reg_trans(operands[1])
            elif len(operands) < 3:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        elif opcode in (0x6,0x7): #bgtz gltz
            if len(operands) == 2:
                if operands[1] in self._symbol_table:
                    imme = origin_to_complement((self._symbol_table[operands[1]] - current_addr - 4)>>2,16)   
                else:
                    try:
                        imme = origin_to_complement(int(operands[2],16)>>2,16)
                    except (ValueError,NumberError):
                        raise InvalidLabel(operands[2])
                rs = self._reg_trans(operands[0])
                rt = 0
            elif len(operands) < 2:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)   
        elif opcode == 0xf: #lui
            if len(operands) == 2:
                imme = str_to_num(operands[1])
                rt = self._reg_trans(operands[0])
                rs = 0
            elif len(operands) < 2:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        else:
            if len(operands) == 3:   
                imme = str_to_num(operands[2],16)
                rt = self._reg_trans(operands[0])
                rs = self._reg_trans(operands[1])
            elif len(operands) < 3:
                raise TooFewOperands(operation)
            else:
                raise TooMuchOperands(operation)
        return (opcode<<26) + (rs<<21) + (rt<<16) + imme


    def _j_type_asm_to_bin(self,operation,operands):
        opcode = self._J_TYPE_DICT[operation]
        if len(operands) == 1:
            if operands[0] in self._symbol_table:
                # 32 bit unsigned number 
                imme = origin_to_complement(self._symbol_table[operands[0]],33)
            else:
                try:
                    imme = origin_to_complement(int(operands[0],16),33)
                except (ValueError,NumberError):
                    raise InvalidLabel(operands[0])
        elif len(operands) < 1:
            raise TooFewOperands(operation)
        else:
            raise TooMuchOperands(operation)
        return (opcode<<26) + (imme>>2)


    def _reg_trans(self,reg_str):
        '''
            :param string
            :return int(0<= <=31)
        '''
        reg_str = reg_str.lower()
        if reg_str[0] == "$":
            reg_name = reg_str[1:]
            if reg_name in self._REG_DICT:
                return self._REG_DICT[reg_name]
            else:
                try:
                    reg_index = int(reg_str[1:],10)
                except ValueError:
                    raise IncorrectRegName(reg_str)
                if reg_index < 0 or reg_index > 31:
                    raise IncorrectRegName(reg_str)
                return reg_index
                
if __name__ == "__main__":
    instruction_translater = InstructionTrans()
    asm_string = input("input a line of assemble instruction: ")
    asm_in_list = split_op(asm_string)
    for x in asm_in_list:
        try:
            result_in_int = instruction_translater.asm_to_bin(x)
        except Error as e: 
           print(e.info)
           print(e.bug)
           raise e
        binary_string = bin(result_in_int)[2:]
        while len(binary_string) < 32:
            binary_string = "0" + binary_string
        print(binary_string)
