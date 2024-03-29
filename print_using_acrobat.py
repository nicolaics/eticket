import win32print
import win32api
import win32con
from tkinter import messagebox

def print_using_acrobat(file_name, printer_name, copy : int, orientation, length, width):
    PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
    printer_handler = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
    level = 2
    properties = win32print.GetPrinter(printer_handler, level)
    pDevModeObj = properties["pDevMode"]

    if orientation == 'P':
        properties["pDevMode"].Orientation = win32con.DMORIENT_PORTRAIT # Change into landscape    
    else:
        properties["pDevMode"].Orientation = win32con.DMORIENT_LANDSCAPE # Change into landscape
    
    # properties["pDevMode"].PaperLength = 500 #SIZE IN 1/10 mm
    # properties["pDevMode"].PaperWidth = 740 #SIZE IN 1/10 mm
        
    properties["pDevMode"].PaperLength = int(length * 100.0) # Size in cm
    properties["pDevMode"].PaperWidth = int(width * 100.0) # Size in cm

    # print(dir(pDevModeObj))
    # print(pDevModeObj.Copies)

    # properties["pDevMode"] = pDevModeObj

    # print(pDevModeObj.PrintQuality)
    # print(pDevModeObj.Color)

    win32print.SetPrinter(printer_handler, level, properties, 0)

    # win32print.DocumentProperties(None, printer_handler, printer_name, pDevModeObj, pDevModeObj, win32con.DM_IN_PROMPT | win32con.DM_IN_BUFFER | win32con.DM_OUT_BUFFER)
    # win32print.DocumentProperties(None, printer_handler, printer_name, pDevModeObj, pDevModeObj, win32con.DM_IN_BUFFER | win32con.DM_OUT_BUFFER)

    for it in range(copy):
        win32api.ShellExecute(
                0,
                "printto",
                file_name,
                '"%s"' % printer_name,
                ".",
                0
            )
    
    win32print.ClosePrinter(printer_handler)

    messagebox.showinfo("Printing", "Now Printing...")

if __name__ == "__main__":
    file_path = r"D:/etiket_2024-01-29/54_Sagsdgjmkn_29-01-2024.pdf"
    # file_path = "trial_7x5.pdf"
    
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)

    count = 1
    for it in printers:
        print(count, ". ", it[2])
        count += 1

    # select = int(input("Select: ")) - 1
    select = 0
    printer_name = printers[select][2]


    print_using_acrobat(file_path, printer_name, 2)