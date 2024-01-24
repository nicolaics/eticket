import win32print
import win32api

file_path = r"D:\etiket_22-01-2024\1_Dewi_22-01-2024.pdf"

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
# printers = win32print.EnumPrinters(2)

# for printer in printers:
#     print(printer)

printer_name = printers[5][2]

win32api.ShellExecute(
        0,
        "printto",
        file_path,
        '"%s"' % printer_name,
        ".",
        0
    )