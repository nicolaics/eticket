import win32print
import win32api
from tkinter import messagebox

def print_using_acrobat(file_name):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    # printers = win32print.EnumPrinters(2)

    # for printer in printers:
    #     print(printer)

    printer_name = printers[5][2]

    win32api.ShellExecute(
            0,
            "printto",
            file_name,
            '"%s"' % printer_name,
            ".",
            0
        )

    messagebox.showinfo("Finished", "Successfully Printed!")

if __name__ == "__main__":
    file_path = r"D:/etiket_25-01-2024/123_Christian suhalim_25-01-2024.pdf"
    print_using_acrobat(file_path)