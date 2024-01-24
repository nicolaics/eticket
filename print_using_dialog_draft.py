import win32print
import win32api

DM_OUT_BUFFER = 0x02
DM_IN_BUFFER = 0x08
DM_IN_PROMPT = 0x04
DM_DEFAULT_SOURCE = 0x200

file_path = r"D:\etiket_22-01-2024\1_Dewi_22-01-2024.pdf"

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)

printer_name = printers[5][2]

PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
printer_handler = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
level = 2
properties = win32print.GetPrinter(printer_handler, level)
pDevModeObj = properties["pDevMode"]

# print(pDevModeObj.PaperWidth)
# print(pDevModeObj.PaperLength)
# print(pDevModeObj.PaperSize)

pDevModeObj.PaperSize = 1
pDevModeObj.PaperLength = 6000 #SIZE IN 1/10 mm
pDevModeObj.PaperWidth = 7000 #SIZE IN 1/10 mm

win32print.DocumentProperties(None, printer_handler, printer_name, pDevModeObj, pDevModeObj, DM_IN_PROMPT | DM_IN_BUFFER | DM_OUT_BUFFER)

# print(pDevModeObj.PaperWidth)
# print(pDevModeObj.PaperLength)
# print(pDevModeObj.PaperSize)

properties["pDevMode"] = pDevModeObj
win32print.SetPrinter(printer_handler, level, properties, 0)

win32api.ShellExecute(
        0,
        "printto",
        file_path,
        '"%s"' % printer_name,
        ".",
        0
    )

win32print.ClosePrinter(printer_handler)