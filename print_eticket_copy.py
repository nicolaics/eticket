import win32print
from datetime import date
import os

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)

# print(printers[5][2])
# for printer in printers:
#     print(printer)

printer_name = printers[5][2]

today = date.strftime(date.today(), "%d-%m-%Y")

parent_dir = "D:/"
directory = "etiket_{0}".format(today)

path = os.path.join(parent_dir, directory)


file_path = r"D:\etiket_22-01-2024\1_Dewi_22-01-2024.pdf"
fh = open(file_path, 'rb')

printer_handler = win32print.OpenPrinter(printer_name)
printer_info = win32print.GetPrinter(printer_handler, 2)
job_info = win32print.StartDocPrinter(printer_handler, 1, (file_path, None, "RAW"))

win32print.StartPagePrinter(printer_handler)
win32print.WritePrinter(printer_handler, fh.read())
win32print.EndPagePrinter(printer_handler)
win32print.EndDocPrinter(printer_handler)

win32print.ClosePrinter(printer_handler)
fh.close()