# -*- coding: utf-8 -*-
from assemble import *
from error import *
from filefilter import *
import sys


if __name__ == "__main__":
    if len(sys.argv) == 2:
        source_file_name = sys.argv[1]
        _type,_name = file_name_parse(source_file_name)
        output_file_name = generate_output_file_name(source_file_name,"BINARY_FILE") 
        with open(output_file_name,"wb") as fp:
            try:
                asm_to_bytes(source_file_name,fp)
            except Error as e:
                print(source_file_name+":"+str(e.position)+":0: "+e.bug+": "+e.info)
    else:
        raise InvalidFilename(sys.argv)

