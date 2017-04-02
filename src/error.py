class Error(Exception):
    def __init__(self):
        Exception.__init__(self)

class DebugError(Error):
    pass

class AssembleError(Error):
    pass
class DisassembleError(Error):
    pass

class PreParseError(AssembleError):
    pass 

class TranslateError(AssembleError):
    pass

class InvalidFileFormat(DisassembleError):
    def __init__(self,filename):
        self.bug = filename
        self.info = "file format is not correct for disassembling"

class InvalidFilename(AssembleError):
    def __init__(self,filename):
        self.bug = filename
        self.info = "program does not recognize this kind of file"

class DuplicateLabel(PreParseError):
    def __init__(self,line,label):
        super().__init__()
        self.info = "label duplicated"
        self.bug = label
        self.position = line

class PesudoInstFault(PreParseError):
    def __init(self,line,instruction):
        super().__init__()
        self.info = "incorrect pesudo instruction"
        self.bug = instruction
        self.position = line

class SegmentNotSpecified(PreParseError):
    def __init__(self,line,instruction):
        super().__init__()
        self.info = "can not find a segment spefication before instruction"
        self.bug = instruction
        self.position = line

class SegmentCollision(TranslateError):
    def __init__(self,inst,seg_addr):
        super().__init__()
        self.info = "segment collide"
        self.bug = seg_addr
        self.position = inst

class InvalidDataFormat(PreParseError):
    def __init__(self,data):
        super().__init__()
        self.bug = data
        self.info = "incorrect data value"
    def add_position_info(self,p_info):
        self.position = p_info

class NumberError(TranslateError):
    def __init__(self,num_st):
        super().__init__()
        self.info = "incorrect number format or number exceed 16 bits"
        self.bug = num_st
    def add_position_info(self,p_info):
        self.position = p_info

class InvalidInstruction(TranslateError):
    def __init__(self,opcode):
        super().__init__()
        self.info = "invaild opcode in instruction"
        self.bug = opcode
    def add_position_info(self,p_info):
        self.position = p_info

class IncorrectRegName(TranslateError):
    def __init__(self,reg_name):
        super().__init__()
        self.info = "incorrect register name."
        self.bug = reg_name
    def add_position_info(self,p_info):
        self.position = p_info

class InvalidLabel(TranslateError):
    def __init__(self,label):
        super().__init__()
        self.info = "invalid label."
        self.bug = label
    def add_position_info(self,p_info):
        self.position = p_info

class TooMuchOperands(TranslateError):
    def __init__(self,operation):
        super().__init__()
        self.info = "too much operands for this operation."
        self.bug = operation
    def add_position_info(self,p_info):
        self.position = p_info

class TooFewOperands(TranslateError):
    def __init__(self,operation):
        super().__init__()
        self.info = "too few operands for this operation"
        self.bug = operation
    def add_position_info(self,p_info):
        self.position = p_info





class InvaidDataToWritten(DebugError):
    def __init__(self,problem_addr):
        super().__init__()
        self.problem_addr = problem_addr
    def __str__(self):
        return "Invaild data written into %s" % self.problem_addr

class InvaidAddrToAccess(DebugError):
    def __init__(self,problem_addr):
        super().__init__()
        self.problem_addr = problem_addr
    def __str__(self):
        return "Invaid address #%s# to access" % self.problem_addr
