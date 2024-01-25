import win32print

def select_printer():
    printers = win32print.EnumPrinters(2)

    index = 0

    for index in range(len(printers)):
        print("{0}. {1}".format((index + 1), printers[index][2]))


    select = int(input("Select your printer: "))
    select -= 1

    print(printers[select][2])

    printer_name = printers[select][2]

    return printer_name
    # for printer in printers:
    #     print(printer)

    # print()
    # print(printers[5][2])


if __name__ == "__main__":
    select_printer()