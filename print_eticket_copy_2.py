import tempfile
import win32api
import win32print

pdf_file = tempfile.mktemp(".pdf")

#CREATION OF PDF FILE WITH REPORTLAB

printer = win32print.GetDefaultPrinter()
PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
pHandle = win32print.OpenPrinter(printer, PRINTER_DEFAULTS)
level = 2
properties = win32print.GetPrinter(pHandle, level)
pDevModeObj = properties["pDevMode"]

pDevModeObj.PaperSize = 0
pDevModeObj.PaperLength = 2200 #SIZE IN 1/10 mm
pDevModeObj.PaperWidth = 1000 #SIZE IN 1/10 mm

properties["pDevMode"]=pDevModeObj
win32print.SetPrinter(pHandle,level,properties,0)
    
#OPTION ONE
#win32api.ShellExecute(0, "print", pdf_file, None, ".", 0)

#OPTION TWO
win32api.ShellExecute (0,"printto",pdf_file,'"%s"' % printer,".",0)

win32print.ClosePrinter(pHandle)