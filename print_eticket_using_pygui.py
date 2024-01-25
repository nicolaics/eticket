import win32print
import win32api
import win32gui

DM_OUT_BUFFER = 0x02
DM_IN_BUFFER = 0x08
DM_IN_PROMPT = 0x04
DM_DEFAULT_SOURCE = 0x200


file_path = "trial.pdf"

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
# printers = win32print.EnumPrinters(2)

# for printer in printers:
#     print(printer)

printer_name = printers[5][2]

# win32print.SetDefaultPrinter(printer_name)

PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
printer_handler = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
level = 2
properties = win32print.GetPrinter(printer_handler, level)
pDevModeObj = properties["pDevMode"]

print(pDevModeObj.PaperWidth)
print(pDevModeObj.PaperLength)
print(pDevModeObj.PaperSize)

# win32print.DocumentProperties

pDevModeObj.PaperSize = 0
pDevModeObj.PaperLength = 7000 #SIZE IN 1/10 mm
pDevModeObj.PaperWidth = 6000 #SIZE IN 1/10 mm

# win32print.DocumentProperties(None, printer_handler, printer_name, pDevModeObj, pDevModeObj, DM_IN_BUFFER | DM_OUT_BUFFER)

# print(pDevModeObj.PaperWidth)
# print(pDevModeObj.PaperLength)
# print(pDevModeObj.PaperSize)

# properties["pDevMode"] = pDevModeObj
# win32print.SetPrinter(printer_handler, level, properties, 0)

# win32api.ShellExecute (0, "printto", file_path,'"%s"' % printer_name,".",0)


hdc = win32gui.CreateDC('', printer_handler, pDevModeObj)

doc_info = (
    "Test",     # doc name
    None,       # name of output file
    "RAW",      # doc type
    0
)
win32print.StartDoc(hdc, doc_info)

# win32print.StartDoc(hdc, ('Test', None, None, 0))
# win32print.StartPage(hdc)
# win32print.WritePrinter(printer_handler, file_path)
# win32print.EndPage(hdc)
# win32print.EndDoc(hdc)

# win32print.ClosePrinter(printer_handler)


# win32api.ShellExecute(0,              # NULL since it's not associated with a window
#              "print",        # execute the "print" verb defined for the file type
#              file_path,  # path to the document file to print
#              None,           #no parameters, since the target is a document file
#              ".",            #current directory, same as NULL here
#              0)              # SW_HIDE passed to app associated with the file type 




# print(printers[5][2])




# today = date.strftime(date.today(), "%d-%m-%Y")

# parent_dir = "D:/"
# directory = "etiket_{0}".format(today)

# path = os.path.join(parent_dir, directory)


# fh = open(file_path, 'rb')

# printer_handler = win32print.OpenPrinter(printer_name)
# printer_info = win32print.GetPrinter(printer_handler, 2)
# job_info = win32print.StartDocPrinter(printer_handler, 1, (file_path, None, "RAW"))

# win32print.StartPagePrinter(printer_handler)
# win32print.WritePrinter(printer_handler, fh.read())
# win32print.EndPagePrinter(printer_handler)
# win32print.EndDocPrinter(printer_handler)

# win32print.ClosePrinter(printer_handler)
# fh.close()