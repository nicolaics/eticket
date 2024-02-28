import win32print
from tkinter import *

def ok_button_clicked(event=None):
    global printer_name_etix
    global select_printer_state_etix
    printer_name_etix = select_printer_state_etix.get()

    global etix_sz
    global etix_sz_state
    etix_sz = etix_sz_state.get()

    printer_def = "prev_printer.txt"
    fh = open(printer_def, 'w')

    fh.write(printer_name_etix + ";")
    fh.write(etix_sz)

    fh.close()

    select_printer_window.quit()
    select_printer_window.destroy()
    
def select_printer(root):
    printers = win32print.EnumPrinters(2)

    global select_printer_window
    select_printer_window = Toplevel(root)
    select_printer_window.title("Pilih Printer dan Size Etiket")
    select_printer_window.geometry("450x300")
    select_printer_window.option_add("*font", "Arial 12")
    select_printer_window.focus_set()

    printer_choice = []

    for printer in printers:
        printer_choice.append(printer[2])
    
    global select_printer_state_etix
    select_printer_state_etix = StringVar()
    
    select_printer_etix_label = Label(select_printer_window, text="Pilih printer untuk ETIKET:")
    select_printer_etix_label.pack(pady=10)
    
    printer_etix_dropdown = OptionMenu(select_printer_window, select_printer_state_etix, *(printer_choice))
    printer_etix_dropdown.config(width=40, background='#DEDBD2', activebackground='white', takefocus=1)
    printer_etix_dropdown.pack()

    global etix_sz_state
    etix_sz_state = StringVar()
    
    etix_sz_label = Label(select_printer_window, text="Pilih ukuran ETIKET:")
    etix_sz_label.pack(pady=10)

    etix_sz_choice = ["7x4", "7x5", "8x3", "8x4"]

    etix_sz_dropdown = OptionMenu(select_printer_window, etix_sz_state, *(etix_sz_choice))
    etix_sz_dropdown.config(width=40, background='#DEDBD2', activebackground='white', takefocus=1)
    etix_sz_dropdown.pack()

    ok_button = Button(select_printer_window, text="Ok", background='#C7EFCF', activebackground='#5ADBFF', command=ok_button_clicked)
    ok_button.pack(pady=20)

    select_printer_window.bind('<Return>', ok_button_clicked)

    global printer_name_presc
    global printer_name_etix
    global etix_sz

    def_printer_file = "prev_printer.txt"
    printer_name_presc = ""
    printer_name_etix = ""
    etix_sz = ""

    try:
        fh = open(def_printer_file, 'r')
        from_file = fh.read().split(";")
        fh.close()

        for index_etix in range(len(printer_choice)):
            if printer_choice[index_etix] == from_file[0]:
                select_printer_state_etix.set(printer_choice[index_etix])
                break
        
        for index_etix_sz in range(len(etix_sz_choice)):
            if etix_sz_choice[index_etix_sz] == from_file[1]:
                etix_sz_state.set(etix_sz_choice[index_etix_sz])
                break
    except:
        pass

    select_printer_window.mainloop()

    return (printer_name_etix, etix_sz)


if __name__ == "__main__":
    root = Tk()
    root.geometry("730x500")
    root.title("Etiket")
    root.option_add("*font", "Arial 14")

    (presc, etix_sz) = select_printer(root)

    if presc == "":
        print("In")
    # print(presc)
    # print(etix_sz)
        
    if etix_sz == "":
        print("In")