# MIPS assembler

### How to use
    choose either 'console' or 'graphics' to run the assembler
1. console.py can be add into sublime as a build system 
    - tool -> build system -> new build system
    - add .json code in Appendix
2. the instruction of graphics.py see "doc/instruction"

### TODO
1. graphic interface will be polished
2. disassemble function will soon be available
3. DEBUG module will be developed 
4. a integrated sublime plug-in may be developed 

### Referrence
1. [mips syntax](https://github.com/contradictioned/mips-syntax)
2. [highlight text](http://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget)

### Appendix
``` json
{
    "cmd": ["python","[your_console.py_path]", "$file"],
    "file_regex": "^(...*?):([0-9]*):([0-9]*): (...*?)$",
    "working_dir": "$file_path",
    "selector": "source.asm"
}
```

