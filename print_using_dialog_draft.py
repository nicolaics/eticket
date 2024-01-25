import win32print
import win32api

from ctypes import windll

from tkinter import messagebox

def print_using_dialog(file_name):
    DM_OUT_BUFFER = 0x02
    DM_IN_BUFFER = 0x08
    DM_IN_PROMPT = 0x04
    DM_DEFAULT_SOURCE = 0x200

    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)

    printer_name = printers[5][2]

    PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
    printer_handler = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)

    # print(dir(printer_handler))

    level = 2
    # level = 8
    properties = win32print.GetPrinter(printer_handler, level)

    # print(properties)
    # print(dir(properties["pDevMode"]))


    # 'Color', 'Copies', 'DefaultSource', 'DeviceName', 'DisplayFixedOutput', 'DisplayFlags', 'DisplayFrequency', 'DisplayOrientation'

    # 'Fields'

    # 'Orientation'
    # 'PaperLength', 'PaperSize', 'PaperWidth'

    # 'PrintQuality'

    # 'Scale', 'Size'

    # print(properties["pSecurityDescriptor"].GetSecurityDescriptorControl())

    pDevModeObj = properties["pDevMode"]

    # print(dir(pDevModeObj))

    # print(pDevModeObj.PaperWidth)
    # print(pDevModeObj.PaperLength)
    # print(pDevModeObj.PaperSize)

    # pDevModeObj.PaperSize = 1
    pDevModeObj.PaperLength = 6000 #SIZE IN 1/10 mm
    pDevModeObj.PaperWidth = 7000 #SIZE IN 1/10 mm

    properties["pDevMode"] = pDevModeObj
    win32print.SetPrinter(printer_handler, level, properties, 0)

    win32print.DocumentProperties(0, printer_handler, printer_name, pDevModeObj, pDevModeObj, DM_IN_PROMPT | DM_IN_BUFFER | DM_OUT_BUFFER)

    properties = win32print.GetPrinter(printer_handler, level)
    
    devmode = properties["pDevMode"]
    for n in dir(devmode):
        print("%s\t%s" % (n, getattr(devmode, n)))

    # windll['winspool.drv'].AdvancedDocumentPropertiesA(None, printer_handler.handle, printer_name, None, None)

    # print(pDevModeObj.PaperWidth)
    # print(pDevModeObj.PaperLength)
    # print(pDevModeObj.PaperSize)

    # properties["pDevMode"] = pDevModeObj
    # win32print.SetPrinter(printer_handler, level, properties, 0)

    # win32api.ShellExecute(
    #         0,
    #         "printto",
    #         file_name,
    #         '"%s"' % printer_name,
    #         ".",
    #         0
    #     )

    win32print.ClosePrinter(printer_handler)

    # messagebox.showinfo("Finished", "Successfully Printed!")

if __name__ == "__main__":
    file_path = r"D:/etiket_25-01-2024/123_Christian suhalim_25-01-2024.pdf"
    print_using_dialog(file_path)