# MIPS assembler

### how to use
    choose either 'console' or 'graphics' to run the assembler
1. console.py can be add into sublime as a build system 
    - tool -> build system -> new build system
    - add .json code in Appendix
2. syntax of MIPS:
    - .text: [*begin_address_in_hex*] //tag the begining of a code segment
    - .data: [*begin_address_in_hex*] //tag the begining of a data segment
    - .word  // 32bits data 
    - .dword // 64bits data
    - .byte  // 8bits data
    - // registers and instructions goes with the standard MIPS syntax
    - // MIPS syntax plug-in for sublime [www.github.com](https://github.com/contradictioned/mips-syntax)

### TODO
1. graphic interface will be polished
2. disassemble function will soon be available
3. DEBUG module will be developed 
4. a integrated sublime plug-in may be developed 



### Appendix
``` json
{
    "cmd": ["python","[your_console.py_path]", "$file"],
    "file_regex": "^(...*?):([0-9]*):([0-9]*): (...*?)$",
    "working_dir": "$file_path",
    "selector": "source.asm"
}
```

