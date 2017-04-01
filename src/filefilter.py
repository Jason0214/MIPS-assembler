from error import *

BINARY_FILE = 0
COE_FILE = 1
ASM_FILE = 2

def file_name_parse(file_path):
    # find the last slash
    slash_index = file_path.rfind("/")
    name = file_path[slash_index+1:]
    # find the extension name
    dot_index = name.rfind(".")
    if dot_index == -1:
        return BINARY_FILE,name
    elif name[dot_index+1:] == "bin":
        return BINARY_FILE,name
    elif name[dot_index+1:] == "asm":
        return ASM_FILE,name
    elif name[dot_index+1:] == "coe":
        return COE_FILE,name
    else:
        raise InvalidFilename(file_path)

def generate_output_file_name(src_file_name,src_file_type):
    dot_index = src_file_name.rfind(".")
    name_without_ext = src_file_name[:dot_index]
    if src_file_type == BINARY_FILE:
        return name_without_ext + ".bin"
    if src_file_type == COE_FILE:
        return name_without_ext + ".coe"
    if src_file_name == ASM_FILE:
        return name_without_ext + ".asm"

    