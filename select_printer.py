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
    select_printer_window.geometry("450x200")
    select_printer_window.option_add("*font", "Arial 12")

    global select_printer_state
    select_printer_state = StringVar()
    
    select_printer_label = Label(select_printer_window, text="Select Printer:")
    select_printer_label.pack()

    printer_choice = []

    for printer in printers:
        printer_choice.append(printer[2])

    printer_dropdown = OptionMenu(select_printer_window, select_printer_state, *(printer_choice))
    printer_dropdown.config(width=40, background='#DEDBD2', activebackground='white', takefocus=1)
    printer_dropdown.pack(pady=20)

    ok_button = Button(select_printer_window, text="Ok", command=ok_button_clicked, background='#C7EFCF', activebackground='#5ADBFF')
    ok_button.pack()

    global printer_name

    select_printer_window.mainloop()

    return printer_name


if __name__ == "__main__":
    root = Tk()
    root.geometry("730x500")
    root.title("Etiket")
    root.option_add("*font", "Arial 14")

    select_printer(root)