from error import *
from number_trans import *


def disassemble(src_file_name,output_file_pointer):
    translater = Binary_Trans()
    temp_bytes = b''
    with open(src_file_name,"rb") as fp:
        while True:
            try:
                temp_bytes = fp.read(4)
            except Exception:
                raise InvaidFileFormat(src_file_name)
            # end of the file
            if not temp_bytes:
                break
            output_file_pointer.write(translater.bin_to_asm(temp_bytes)+"\n")

class Binary_Trans:
    def __init__(self):
        self._REG_DICT = {0:"$zero",1:"$at",2:"$v0",3:"$v1",4:"$a0",5:"$a1",6:"$a2",7:"$a3",8:"$t0",9:"$t1",10:"$t2",11:"$t3",12:"$t4",13:"$t5",14:"$t6",15:"$t7",
                          16:"$s0",17:"$s1",18:"$s2",19:"$s3",20:"$s4",21:"$s5",22:"$s6",23:"$s7",24:"$t8",25:"$t9",26:"$k0",27:"$k1",28:"$gp",29:"$sp",30:"$fp",31:"$ra"}
        self._R_TYPE_INST = {0x20:"add",0x21:"addu",0x22:"sub",0x23:"subu",0x24:"and",0x25:"or",0x26:"xor",0x27:"nor",0x8:"jr",0x9:"jalr",
                            0x4:"sllv",0x6:"srlv",0x7:"srav",0x2a:"slt",0x21:"sltu",0x0:"sll",0x02:"srl",0x3:"sra"}
        self._I_TYPE_INST = {0x8:"addi",0x9:"addiu",0xd:"ori",0xc:"andi",0xe:"xori",0xf:"lui",0xa:"slti",0xb:"sltiu",0x23:"lw",0x20:"lb",0x24:"lbu",0x21:"lh",0x25:"lhu",
                            0x2b:"sw",0x29:"sh",0x28:"sb",0x4:"beq",0x5:"bne",0x7:"bgtz",0x6:"blez"}
        self._J_TYPE_INST = {0x3:"jal",0x2:"j"}
    def bin_to_asm(self,bytes_obj):
        binary_num = int.from_bytes(bytes_obj,"big")
        opcode = binary_num >> 26
        if opcode == 0:
            return self._r_type_trans(binary_num)
        elif opcode in self._I_TYPE_INST:
            return self._i_type_trans(opcode, binary_num)
        elif opcode in self._J_TYPE_INST:
            return self._j_type_trans(opcode, binary_num)
        else:
            return ".dword "+int_to_hex(binary_num)

    def _r_type_trans(self, bin_num):
        bin_num_cut_from_func = bin_num >> 6
        bin_num_cut_from_shamt = bin_num_cut_from_func >> 5
        bin_num_cut_from_rd = bin_num_cut_from_shamt >> 5
        bin_num_cut_from_rt = bin_num_cut_from_rd >> 5
        bin_num_cut_from_rs = bin_num_cut_from_rt >> 5
        #
        func = bin_num - (bin_num_cut_from_func << 6)
        shamt = bin_num_cut_from_func - (bin_num_cut_from_shamt << 5)
        rd = bin_num_cut_from_shamt - (bin_num_cut_from_rd << 5)
        rt = bin_num_cut_from_rd - (bin_num_cut_from_rt << 5)
        rs = bin_num_cut_from_rt - (bin_num_cut_from_rs << 5)
        try:
            operation = self._R_TYPE_INST[func]
            rd = self._REG_DICT[rd]
            if func in (0x0,0x2,0x3):
                rt = self._REG_DICT[rt]
                return operation+" "+rd+", "+rt+", "+hex(shamt)
            elif func in (0x8,0x9):
                return operation+" "+rd
            else:
                rt = self._REG_DICT[rt]
                rs = self._REG_DICT[rs]
                return operation+" "+rd+", "+rs+", "+rt
        except KeyError:
            return ".dword "+int_to_hex(bin_num)

    def _i_type_trans(self,opcode,bin_num):
        operation = self._I_TYPE_INST[opcode]
        #
        bin_num_cut_from_imme = bin_num >> 16;
        bin_num_cut_from_rt = bin_num_cut_from_imme >> 5
        bin_num_cut_from_rs = bin_num_cut_from_rt >> 5
        #
        imme = bin_num - (bin_num_cut_from_imme << 16)
        rt = bin_num_cut_from_imme - (bin_num_cut_from_rt << 5)
        rs = bin_num_cut_from_rt - (bin_num_cut_from_rs << 5)
        operation = self._I_TYPE_INST[opcode]
        try:
            rs = self._REG_DICT[rs]
            if opcode in (0x23,0x20,0x24,0x21,0x25,0x2b,0x28,0x29):
                rt = self._REG_DICT[rt]            
                return operation+" "+rt+", "+str(imme)+"("+rs+")"
            elif opcode in (0x4,0x5):# branch
                rt = self._REG_DICT[rt]
                return operation+" "+rt+", "+rs+", "+hex(imme << 2)
            elif opcode in (0x6,0x7):# branch
                return operation+" "+rs+", "+hex(imme << 2)
            else:
                rt = self._REG_DICT[rt]
                return operation+" "+rt+", "+rs+", "+hex(imme)
        except KeyError:
            return ".dword "+int_to_hex(bin_num)


    def _j_type_trans(self,opcode,bin_num):
        operation = self._J_TYPE_INST[opcode]
        target = bin_num - (bin_num >> 26 << 26)
        return operation +" "+hex(target)


if __name__ == "__main__":
    import binascii
    translater = Binary_Trans()
    byte = binascii.unhexlify(input("hex string: "))
    print(translater.bin_to_asm(byte))