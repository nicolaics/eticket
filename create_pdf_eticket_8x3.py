from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date

import os

def get_num_of_lines_in_multicell(pdf, message, width, err_margin):
    # divide the string in words
    words = message.split(" ")
    line = ""
    n = 1

    for word in words:
        line += word + " "
        line_width = pdf.get_string_width(line)

        if line_width > width - err_margin:
            # the multi_cell() insert a line break
            n += 1
            # reset of the string
            line = word + " "
    return n

def create_pdf_eticket_8x3(data):
    PAPER_WIDTH = 8
    PAPER_HEIGHT = 3

    BOLD = "B"
    REGULAR = ""
    FONT_SIZE = 9
    BIGGER_FONT_SIZE = 11
    CELL_HEIGHT = 0.6
    MARGIN = 0.1
    MAX_WIDTH = PAPER_WIDTH - (MARGIN * 2)

    today = date.strftime(date.today(), "%d-%m-%Y")
    today_folder = date.today()

    parent_dir = "D:/"
    directory = "etiket_{0}".format(today_folder)

    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
    except:
        pass

    pdf = FPDF('P', 'cm', (PAPER_WIDTH, PAPER_HEIGHT))
    pdf.set_margins(MARGIN, 0, MARGIN)
    pdf.set_auto_page_break(False, MARGIN)


    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
    FONT_NAME = "Arial"

    # Add page
    pdf.add_page()
    
    FIRST_COL_WIDTH = PAPER_WIDTH / 3

    pdf.set_line_width(0.02)

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    num_col_width = pdf.get_string_width("No. {0}".format(data["num"])) + MARGIN
    pdf.cell(num_col_width, CELL_HEIGHT, "No. {0}".format(data["num"]), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Line after No.
    pdf.line(0, pdf.y, FIRST_COL_WIDTH, pdf.y)

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    date_col_width = pdf.get_string_width("Tgl. {0}".format(today)) + MARGIN
    pdf.cell(date_col_width, CELL_HEIGHT, "Tgl. {0}".format(today), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    date_name_line_y = pdf.y

    # Line after Date and Name
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    # Vertical divide line
    pdf.line(FIRST_COL_WIDTH, 0, FIRST_COL_WIDTH, pdf.y)

    # Set "Nama:" to be in the middle
    name_col_width = pdf.get_string_width("Nama:") + MARGIN

    pdf.set_xy((FIRST_COL_WIDTH + MARGIN), (CELL_HEIGHT / 2))
    pdf.cell(name_col_width, CELL_HEIGHT, "Nama:")

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    name_size_limit = (MAX_WIDTH - FIRST_COL_WIDTH - name_col_width)

    num_of_lines = get_num_of_lines_in_multicell(pdf, data["name"], name_size_limit, 0.3)
    print(num_of_lines)

    if num_of_lines == 1:
        pdf.set_xy(pdf.x, (CELL_HEIGHT / 2))
    else:
        pdf.set_xy(pdf.x, 0)

    pdf.multi_cell((MAX_WIDTH - FIRST_COL_WIDTH - name_col_width), CELL_HEIGHT, data["name"], align='c', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After Name: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)

    pdf.set_y(date_name_line_y)

    pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["use"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Line after usage
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    print("After use: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))
   
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    a_day_width = pdf.get_string_width("Sehari") + MARGIN
    pdf.cell(a_day_width, CELL_HEIGHT, "Sehari")

    consume_y = pdf.y

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)
    pdf.set_xy((pdf.x + MARGIN), (pdf.y + MARGIN))
    pdf.write_html(data["dose"])

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    unit_width = pdf.get_string_width("Bungkus")
    pdf.set_xy(2.4, consume_y)
    pdf.cell(unit_width, CELL_HEIGHT, data["unit"], align='l')

    print("After dose: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    pdf.set_xy((MARGIN + (PAPER_WIDTH / 2)), pdf.y)

    pdf.cell((MAX_WIDTH / 2), CELL_HEIGHT, data["consume_time"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After consume time: {0}, {1:.1f}".format(pdf.x, pdf.y))

    # Dose vertical seperator line
    pdf.line((PAPER_WIDTH / 2), consume_y, (PAPER_WIDTH / 2), (consume_y + CELL_HEIGHT))

    # Line after dose and when to consume
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    if data["must_finish"] == "HABISKAN":
        # Qty and must finish vertical seperator line
        pdf.line((PAPER_WIDTH / 2), pdf.y, (PAPER_WIDTH / 2), (pdf.y + CELL_HEIGHT))

        pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
        pdf.cell(((MAX_WIDTH / 2) - MARGIN), CELL_HEIGHT, "Qty: {0}".format(data["qty"]), align='c')

        pdf.set_xy(((MAX_WIDTH / 2) + MARGIN), pdf.y)
        pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
        pdf.cell(((MAX_WIDTH / 2) - MARGIN), CELL_HEIGHT, data["must_finish"], align='C')
    else:
        pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
        pdf.cell(MAX_WIDTH, CELL_HEIGHT, "Qty: {0}".format(data["qty"]), align='c')

    print("Must finish: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    file_name = path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today)

    # file_name = "8x3.pdf"
    
    print(file_name)
    pdf.output(file_name)

    return (file_name, PAPER_WIDTH, (PAPER_HEIGHT + 0.4), 'P')
    

if __name__ == "__main__":
    data = {
        "num": "69-1",
        "name": "Nicolai Christian Su",
        # "name": "Nicolai",
        # "name": "Seng Kwek Gega",
        "use": "Antibiotik / Radang Tenggorokkan",
        # "use": "Radang Tenggorokkan",
        # "use": "Obat Tidur / PenenangW",
        # "use": "Maag",
        "dose": u"3 x <sup>1</sup>\u2044<sub>2</sub>",
        # "dose": "3 x 1",
        "consume_time": "Sesudah Makan",
        # "must_finish": "Tidak",
        "must_finish": "HABISKAN",
        # "unit": "Kapsul",
        "unit": "Bungkus",
        "qty": "100",
        "date": "30-01-2024"
    }

    create_pdf_eticket_8x3(data)