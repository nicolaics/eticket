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

def create_pdf_eticket_7x4(data):
    PAPER_WIDTH = 4
    PAPER_HEIGHT = 7

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
    pdf.set_margin(MARGIN)
    pdf.set_auto_page_break(False, MARGIN)


    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
    FONT_NAME = "Arial"

    # Add page
    pdf.add_page()
    
    TOP_COLUMN_WIDTH = (PAPER_WIDTH - (2 * MARGIN)) / 2

    pdf.set_line_width(0.02)
    # Top line
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)

    num_col_width = pdf.get_string_width("No.") + MARGIN

    pdf.cell(num_col_width, CELL_HEIGHT, "No.")
    pdf.cell((TOP_COLUMN_WIDTH - num_col_width), CELL_HEIGHT, data["num"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Line after No.
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    date_col_width = pdf.get_string_width("Tgl.") + MARGIN
    pdf.cell(date_col_width, CELL_HEIGHT, "Tgl.")
    pdf.cell((TOP_COLUMN_WIDTH - date_col_width), CELL_HEIGHT, today, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # print("After No. and Date: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after date
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)
    
    # Save temp for the name title and the name itself
    temp_y = pdf.y
    
    # Set the Y-axis for the name title to be in the middle of the box
    pdf.y += 0.7

    name_col_width = pdf.get_string_width("Nama:")

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(name_col_width, None, "Nama:")

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)

    name_size_limit = (MAX_WIDTH - name_col_width)

    num_of_lines = get_num_of_lines_in_multicell(pdf, data["name"], name_size_limit, 0.3)
    # print(num_of_lines)

    # To reset the Y-axis for the name from the title
    pdf.y = temp_y

    if num_of_lines == 1:
        pdf.y += (CELL_HEIGHT / 2) + 0.25
    elif num_of_lines == 2:
        pdf.y += (CELL_HEIGHT / 2)

    pdf.x = name_col_width + (MARGIN * 2)

    pdf.multi_cell((MAX_WIDTH - name_col_width - (MARGIN * 2)), CELL_HEIGHT, data["name"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # print("After Name: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    second_line_y = temp_y + (CELL_HEIGHT * 3)
    pdf.y = second_line_y

    # Line after name
    pdf.line(0, second_line_y, PAPER_WIDTH, second_line_y)

    temp_y = pdf.y
    third_line_y = temp_y + (CELL_HEIGHT * 2)

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)

    num_of_lines = get_num_of_lines_in_multicell(pdf, data["use"], MAX_WIDTH, 0)
    # print(num_of_lines)

    # To put the use in the middle of the box
    if num_of_lines == 1:
        pdf.y += (CELL_HEIGHT / 2)

    pdf.multi_cell(MAX_WIDTH, CELL_HEIGHT, data["use"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # print("After use: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after medicine usage
    pdf.line(0, third_line_y, PAPER_WIDTH, third_line_y)

    pdf.y = third_line_y
    
    fourth_line_y = third_line_y + CELL_HEIGHT

    pdf.set_xy(0.2, third_line_y)
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    title_width = pdf.get_string_width("Sehari")
    pdf.cell(title_width, CELL_HEIGHT, "Sehari")

    unit_width = pdf.get_string_width("Bungkus") + (MARGIN * 2)

    dose_pos_y = third_line_y + MARGIN

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)
    pdf.set_xy(1.3, dose_pos_y)
    pdf.write_html(data["dose"])

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.set_xy(2.5, third_line_y)
    pdf.cell(unit_width, CELL_HEIGHT, data["unit"], align='l', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # print("After dose: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after dose
    pdf.line(0, fourth_line_y, PAPER_WIDTH, fourth_line_y)

    pdf.y = fourth_line_y

    pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["consume_time"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # print("After consume time: {0}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after when to eat the medicine
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)
    
    if data["must_finish"] == "HABISKAN":
        pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
        pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["must_finish"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    # print("Must finish: {0:.1f}, {1:.1f}".format(pdf.x, pdf.y))
    
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(MAX_WIDTH, CELL_HEIGHT, "Qty: {0}".format(data["qty"]), align='c', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    file_name = path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today)
    
    # file_name = "7x4.pdf"
    
    # print(file_name)
    pdf.output(file_name)

    return (file_name, PAPER_WIDTH, (PAPER_HEIGHT + 0.4), 'L')
    

if __name__ == "__main__":
    data = {
        "num": "69-1",
        "name": "Nicolai Chris",
        # "name": "Nicolai",
        # "name": "Seng Kwek Gega",
        # "use": "Antibiotik / Radang Tenggorokan",
        # "use": "Obat Tidur / PenenangW",
        "use": "Maag",
        # "dose": "3 x 1",
        "dose": u"3 x <sup>1</sup>\u2044<sub>2</sub>",
        "consume_time": "Sesudah Makan",
        # "must_finish": "Tidak",
        "must_finish": "HABISKAN",
        # "unit": "Kapsul",
        "unit": "Bungkus",
        "qty": "100"
    }

    create_pdf_eticket_7x4(data)