from tkinter import *
from tkinter import messagebox
from create_pdf_eticket import create_pdf_eticket

LEFT = 'w'
RIGHT = 'e'
TOP = 'n'
BOTTOM = 's'

PADDING = 10

FONT_NAME = "Arial"
FONT_SIZE = 14

global data
data = {}

def null_checking(param_entry, param_state_1, param_state_2):
    for entry in param_entry:
        if entry.get() == "":
            return False
    
    for entry in param_state_1:
        if entry.get() == "":
            return False
        
    for entry in param_state_2:
        if entry.get() == "":
            return False
        
    if medicine_use_other is True:
        if use_others_entry.get() == "":
            return False
    
    return True

def type_checking(string):
    try:
        int(string)
        return True
    except:
        return False
    
def print_button_clicked():
    isValid = null_checking(entry_group, dropdown_state_group, radio_state_group)

    if isValid is False:
        messagebox.showerror("Error", "Ada yang belum di-isi atau dipilih!")
        return

    isValid = type_checking(num_entry.get())

    if isValid is False:
        messagebox.showerror("Error", "Nomor harus angka!")
        return
    else:
        data["num"] = num_entry.get()

    data["name"]=  name_entry.get().capitalize()
    
    isValid = type_checking(num_of_consume_entry.get())
    
    if isValid is False:
        messagebox.showerror("Error", "Berapa kali sehari harus angka!")
        return

    dose = dose_entry.get()

    if dose.find('/') != -1:
        dose_split = dose.split('/')
        dose = u"<b>{0} x <sup>{1}</sup>\u2044<sub>{2}</sub></b>".format(num_of_consume_entry.get(), dose_split[0], dose_split[1])
    else:
        isValid = type_checking(dose)
        
        if isValid is False:
            messagebox.showerror("Error", "Dosis tidak valid!")
            return

        dose = "<b>{0} x {1}</b>".format(num_of_consume_entry.get(), dose)

    data["dose"] = dose
    data["unit"] = unit_state.get()
    data["consume_time"] = consume_time_state.get()

    if must_finish_state.get() == "Ya":
        data["must_finish"] = "Harus Dihabiskan"
    else:
        data["must_finish"] = None

    create_pdf_eticket(data)

    messagebox.showinfo("Printing...", "Now Printing...")

    for entry in entry_group:
        entry.delete(0, 'end')

    for entry in dropdown_state_group:
        entry.set("")

    for entry in radio_state_group:
        entry.set(None)  

def get_med_use(event):
    global use
    global medicine_use_other
    medicine_use_other = False

    if use_state.get() == use_choice[9]:
        medicine_use_other = True

        use_dropdown_menu.grid(row=2, column=1, columnspan=2, sticky=LEFT + RIGHT, pady=PADDING)
        use_others_entry.grid(row=2, column=3, columnspan=2, sticky=LEFT + RIGHT, padx=PADDING, pady=PADDING)
        
        print(use_others_entry.get())
        use = use_others_entry.get().capitalize()
        data["use"] = use
    else:
        use = use_state.get()
        use_others_entry.grid_remove()
        print(use_state.get())
        data["use"] = use

use_choice = [
    "Batuk",
    "Pilek",
    "Batuk dan Pilek",
    "Batuk Sesak",
    "Maag",
    "Sakit / Nyeri",
    "Antibiotik / Radang Tenggorokan",
    "Vitamin",
    "Obat Tidur / Penenang",
    "Yang lain:"
]

unit_choice = [
    "Tablet",
    "Kapsul",
    "Bungkus"
]

consume_time_choice = [
    "Sebelum Makan",
    "Sesudah Makan"
]

root = Tk()
root.geometry("730x500")
root.title("Etiket")
root.option_add("*font", "Arial 14")

root["padx"] = 50
root["pady"] = PADDING

num_label = Label(root, text="No.")
num_label.grid(row=0, column=0, sticky=RIGHT, padx=PADDING, pady=PADDING)

num_entry = Entry(root)
num_entry.grid(row=0, column=1, columnspan=4, sticky=LEFT + RIGHT, pady=PADDING)

name_label = Label(root, text="Nama:")
name_label.grid(row=1, column=0, sticky=RIGHT, padx=PADDING, pady=PADDING)

name_entry = Entry(root)
name_entry.grid(row=1, column=1, columnspan=4, sticky=LEFT + RIGHT, pady=PADDING)

use_label = Label(root, text="Jenis obat:")
use_label.grid(row=2, column=0, sticky=RIGHT, padx=PADDING, pady=PADDING)

use_state = StringVar()

use_dropdown_menu = OptionMenu(root, use_state, *use_choice, command=get_med_use)
use_dropdown_menu.config(background='#DEDBD2', activebackground='white')
use_dropdown_menu.grid(row=2, column=1, columnspan=4, sticky=LEFT + RIGHT, pady=PADDING)

use_others_entry = Entry(root)

num_of_consume_label = Label(root, text="Berapa kali sehari:", wraplength=100, justify='right')
num_of_consume_label.grid(row=3, column=0, sticky=RIGHT, padx=PADDING, pady=PADDING)

num_of_consume_entry = Entry(root, width=10)
num_of_consume_entry.grid(row=3, column=1, pady= PADDING)

times_label = Label(root, text="x")
times_label.grid(row=3, column=2, pady= PADDING)

dose_entry = Entry(root, width=10)
dose_entry.grid(row=3, column=3, padx=PADDING, pady= PADDING)

unit_state = StringVar()

unit_dropdown_menu = OptionMenu(root, unit_state, *unit_choice)
unit_dropdown_menu.config(width=10, background='#DEDBD2', activebackground='white')
unit_dropdown_menu.grid(row=3, column=4, sticky=LEFT + RIGHT, pady=PADDING)

consume_time_label = Label(root, text="Waktu minum:", justify='right')
consume_time_label.grid(row=4, column=0, sticky=RIGHT, pady= PADDING)

consume_time_state = StringVar()
consume_time_state.set(None)

col = 1
for consume_time in consume_time_choice:
    rad_button = Radiobutton(root, text=consume_time, value=consume_time, variable=consume_time_state, justify='left')
    rad_button.grid(row=4, column=col, columnspan=2, sticky=LEFT + RIGHT, pady= PADDING)
    col += 2

must_finish_label = Label(root, text="Harus dihabiskan atau tidak?", wraplength=100, justify='right')
must_finish_label.grid(row=5, column=0, padx=PADDING, pady= PADDING)

must_finish_state = StringVar()
must_finish_state.set(None)

yes_finish_radio_button = Radiobutton(root, text="Ya", value="Ya", variable=must_finish_state, justify='left')
yes_finish_radio_button.grid(row=5, column=1, pady= PADDING)

no_finish_radio_button = Radiobutton(root, text="Tidak", value="Tidak", variable=must_finish_state, justify='left')
no_finish_radio_button.grid(row=5, column=2, pady= PADDING)


entry_group = (num_entry, name_entry, num_of_consume_entry, dose_entry)
dropdown_state_group = (use_state, unit_state)
radio_state_group = (consume_time_state, must_finish_state)
        

print_button = Button(root, text="Print", command=print_button_clicked, background='#C7EFCF', activebackground='#5ADBFF')
print_button.grid(row=6, column=0, columnspan=5, sticky=LEFT + RIGHT, padx=PADDING, pady=PADDING)

root.mainloop()