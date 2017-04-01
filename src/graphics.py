import tkinter
from tkinter import filedialog
from tkinter.constants import *
from assemble import *
from filefilter import *
import binascii

class Top(tkinter.Tk):
    def __init__(self):
        # create window
        tkinter.Tk.__init__(self)
        self.title("MIPS assembler")
        self.geometry('800x600')
        self.resizable(width=False,height=False)
        self.configure(background="WhiteSmoke")
        # create menu
        self.create_menu()
        self.add_widgets()
        # variables for file IO
        self._output_file_type = BINARY_FILE
        self._src_file_type = -1
        self._src_file_path_and_name = ""

    def create_menu(self):
        # menu bar
        self.menu_bar = tkinter.Menu(self)
        self.config(menu=self.menu_bar)
        # file submenu
        filemenu = tkinter.Menu(self.menu_bar,tearoff=0)
        filemenu.add_command(label="open", command=self._open_file)
        filemenu.add_command(label="save", command=self._save_file)
        filemenu.add_separator()
        filemenu.add_command(label="exit", command=self.quit)
        # add file to menu bar
        self.menu_bar.add_cascade(label="File", menu=filemenu)
        # edit submenu
        edit_menu = tkinter.Menu(self.menu_bar,tearoff=0)
        edit_menu.add_command(label="edit", command=self._beg_editting)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # run submenu
        run_menu = tkinter.Menu(self.menu_bar,tearoff=0)
        run_menu.add_command(label="assemble", command=self.assemble)
        run_menu.add_command(label="disassemble", command=self.disassemble)
        self.menu_bar.add_cascade(label="Run", menu=run_menu)

    def assemble(self):
        if self._src_file_type == ASM_FILE:
            output_file = generate_output_file_name(self._src_file_path_and_name,self._output_file_type)               
            if self._output_file_type == BINARY_FILE:
                # assemble
                with open(output_file,"wb") as fp:
                    try:
                        asm_to_bytes(self._src_file_path_and_name,fp)
                    except Error as e:
                        self.append_text(self._console,"[assemble failed: " + e.bug + ": " + e.info +"]\n")
                        return
                # display the result
                with open(output_file,"rb") as fp:
                    bin_str = ""
                    while True:
                        temp = fp.read(4)
                        if len(temp) == 0:
                            break
                        bin_str += int_to_binary(int(binascii.hexlify(temp),16))
                        bin_str += "\n"
                self.output_text(self._right_box,bin_str)
                self.append_text(self._console,"[assemble finished]\n")
            elif self._output_file_type == COE_FILE:
                with open(output_file,"w") as fp:
                    try:
                        asm_to_coe(self._src_file_path_and_name,fp)
                    except Error as e:
                        self.append_text(self._console,"[assemble failed: " + e.bug + ": " + e.info +"]\n")
                        return 
                with open(output_file,"r") as fp:
                    self.output_text(self._right_box,fp.read())
        else:
            pass
    def disassemble(self):
        pass

    def add_widgets(self):
        # specify the current opened file
        self._left_label = tkinter.Label(self,background="WhiteSmoke")
        self._left_label.grid(row=0, column=1,columnspan=3)
        # text area for current opened file, support editting
        self._left_box = tkinter.Text(self, width=60, height=30)
        self._left_box.grid(row=1, column=1, rowspan=2, columnspan=3, padx=20)
        self._left_box.configure(state=DISABLED)
        # text area for results, read only
        self._right_box = tkinter.Text(self, width=40, height=30)
        self._right_box.grid(row=1, column=4, rowspan=2, columnspan=2, padx=20)
        self._right_box.configure(state=DISABLED)
        # console window
        self._console = tkinter.Text(self,width=106, height=8)
        self._console.grid(row =3,column=1,columnspan=5,padx=15,pady=30)
        self.append_text(self._console,"console:\n")
        self._console.configure(state=DISABLED)

    def add_buttons(self):
        if self._src_file_type == ASM_FILE:
            # check buttons for selecting type of output file
            self._bin_button = tkinter.Checkbutton(self,text='.bin',command=self._bin_button_switch)
            self._bin_button.grid(row=0,column=4)
            self._bin_button.select()
            self._coe_button = tkinter.Checkbutton(self,text='.coe',command=self._coe_button_switch)
            self._coe_button.grid(row=0,column=5)
            self._coe_button.deselect()
        else:
            self._asm_button = tkinter.Checkbutton(self,text=".asm")
            self._asm_button.grid(row=0,column=4)
            self._asm_button.select()
            self._asm_button.configure(state=DISABLED)

    def append_text(self,text_widget,string):
        text_widget.configure(state=NORMAL)
        text_widget.insert(END,string)
        text_widget.configure(state=DISABLED)      

    def output_text(self,text_widget,string):
        text_widget.configure(state=NORMAL)
        text_widget.delete(1.0,END)
        text_widget.insert(END,string)
        text_widget.configure(state=DISABLED)

    def _open_file(self):
        self._src_file_path_and_name = filedialog.askopenfilename()
        # split src file name and judge the type of src file
        try:
            self._src_file_type,self._src_file_name = file_name_parse(self._src_file_path_and_name)
        except InvalidFilename as e:
            self.append_text(self._console,"[open failed: "+e.bug+": "+e.info+"]\n")
            self._src_file_path_and_name = ""
            return 
        # change corresponding widgets
        self.append_text(self._console,"[open file: "+self._src_file_path_and_name+"]\n")
        self._left_label.configure(text = self._src_file_name)
        self.add_buttons()
        # output the contain of src file
        with open(self._src_file_path_and_name,"r") as fp:
            self.output_text(self._left_box,fp.read())

    def _save_file(self):
        pass

    def _beg_editting(self):
        self._left_box.configure(state=NORMAL)

    def _bin_button_switch(self):
        self._coe_button.toggle()
        if self._output_file_type == BINARY_FILE:
            self._output_file_type = COE_FILE
        else:
            self._output_file_type = BINARY_FILE

    def _coe_button_switch(self):
        self._bin_button.toggle()
        if self._output_file_type == BINARY_FILE:
            self._output_file_type = COE_FILE
        else:
            self._output_file_type = BINARY_FILE

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    top = Top()
    top.run()

