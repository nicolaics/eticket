import os
import printfactory
import pathlib
from datetime import date

today = date.strftime(date.today(), "%d-%m-%Y")

parent_dir = "D:/"
directory = "etiket_{0}".format(today)

path = os.path.join(parent_dir, directory)

printer = printfactory.Printer()
printfactory.
print_tool = printfactory.AdobeReader(printer)

file = pathlib.Path(r"D:\etiket_22-01-2024\1_Dewi_22-01-2024.pdf")
print_tool.print_file(file)