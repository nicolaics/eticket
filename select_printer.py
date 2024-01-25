import win32print
from tkinter import *

def ok_button_clicked():
    global printer_name
    printer_name = select_printer_state.get()

    printer_def = "def_printer.txt"
    fh = open(printer_def, 'w')

    fh.write(printer_name)
    fh.close()

    select_printer_window.quit()
    select_printer_window.destroy()
    

def select_printer(root):
    printers = win32print.EnumPrinters(2)

    global select_printer_window
    select_printer_window = Toplevel(root)
    select_printer_window.title("Select Printer")
    select_printer_window.geometry("400x300")
    select_printer_window.option_add("*font", "Arial 12")

    global select_printer_state
    select_printer_state = StringVar()
    select_printer_state.set(None)
    
    select_printer_label = Label(select_printer_window, text="Select Printer:")
    select_printer_label.pack()

    for printer in printers:
        radio_button = Radiobutton(select_printer_window, text=printer[2], value=printer[2], variable=select_printer_state, justify='left')
        radio_button.pack()

    ok_button = Button(select_printer_window, text="Ok", command=ok_button_clicked, background='#C7EFCF', activebackground='#5ADBFF')
    ok_button.pack()

    global printer_name

    select_printer_window.mainloop()

    return printer_name


# if __name__ == "__main__":
#     select_printer()