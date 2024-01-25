import win32print
import win32api
from tkinter import messagebox

def print_using_acrobat(file_name, printer_name):
    DM_OUT_BUFFER = 0x02
    DM_IN_BUFFER = 0x08

    PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
    printer_handler = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
    level = 2
    properties = win32print.GetPrinter(printer_handler, level)
    pDevModeObj = properties["pDevMode"]
    
    pDevModeObj.PaperLength = 6000 #SIZE IN 1/10 mm
    pDevModeObj.PaperWidth = 7000 #SIZE IN 1/10 mm
    pDevModeObj.Color = 2
    pDevModeObj.PrintQuality = 100

    properties["pDevMode"] = pDevModeObj

    print(pDevModeObj.PrintQuality)
    print(pDevModeObj.Color)

    win32print.DocumentProperties(None, printer_handler, printer_name, pDevModeObj, pDevModeObj, DM_IN_BUFFER | DM_OUT_BUFFER)

    win32api.ShellExecute(
            0,
            "printto",
            file_name,
            '"%s"' % printer_name,
            ".",
            0
        )
    
    win32print.ClosePrinter(printer_handler)

    messagebox.showinfo("Finished", "Successfully Printed!")

if __name__ == "__main__":
    # file_path = r"D:/etiket_25-01-2024/123_Christian suhalim_25-01-2024.pdf"
    file_path = "trial.pdf"
    
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    printer_name = printers[5][2]


    print_using_acrobat(file_path, printer_name)