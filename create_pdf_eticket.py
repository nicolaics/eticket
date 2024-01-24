from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os

from print_using_acrobat_draft import print_using_acrobat
from print_using_dialog_draft import print_using_dialog

def get_num_of_lines_in_multicell(pdf, message, CELL_WIDTH):
    # divide the string in words
    words = message.split(" ")
    line = ""
    n = 1
    for word in words:
        line += word + " "
        line_width = pdf.get_string_width(line)
        # In the next if it is necessary subtract 1 to the WIDTH
        if line_width > CELL_WIDTH - 1:
            # the multi_cell() insert a line break
            n += 1
            # reset of the string
            line = word + " "
    return n

def create_pdf_eticket(data):
    PAPER_WIDTH = 6
    # PAPER_HEIGHT = 6.5
    PAPER_HEIGHT = 7

    BOLD = "B"
    REGULAR = ""
    FONT_SIZE = 10
    BIGGER_FONT_SIZE = 14
    CELL_HEIGHT = 0.8
    MARGIN = 0.1
    MAX_WIDTH = PAPER_WIDTH - (MARGIN * 2)

    today = date.strftime(date.today(), "%d-%m-%Y")

    parent_dir = "D:/"
    directory = "etiket_{0}".format(today)

    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
    except:
        pass

    pdf = FPDF('P', 'cm', (PAPER_WIDTH, PAPER_HEIGHT))
    # pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_margins(MARGIN, 0.2, MARGIN)
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

    title_width = pdf.get_string_width("No.")
    num_col_width = title_width + MARGIN

    pdf.cell(num_col_width, CELL_HEIGHT, "No.")

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)

    pdf.cell((TOP_COLUMN_WIDTH - num_col_width), CELL_HEIGHT, data["num"])

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    title_width = pdf.get_string_width("Tgl:")
    date_col_width = title_width + MARGIN
    pdf.cell(date_col_width, CELL_HEIGHT, "Tgl:")

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    pdf.cell((TOP_COLUMN_WIDTH - date_col_width), CELL_HEIGHT, today, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After No. and Date: {0}, {1}".format(pdf.x, pdf.y))

    # Line after No. and date
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)
    
    # Save temp for the name title and the name itself
    temp_y = pdf.y
    
    # Set the Y-axis for the name title to be in the middle of the box
    pdf.y += 0.6

    title_width = pdf.get_string_width("Nama:")
    name_col_width = title_width + MARGIN

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(name_col_width, None, "Nama:")

    num_of_lines = get_num_of_lines_in_multicell(pdf, data["name"], (MAX_WIDTH - name_col_width))
    # print(num_of_lines_name)

    # To reset the Y-axis for the name from the title
    pdf.y = temp_y

    if num_of_lines == 1:
        pdf.y += (CELL_HEIGHT / 2)

    pdf.x = name_col_width + MARGIN

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    pdf.multi_cell((MAX_WIDTH - name_col_width - (MARGIN * 2)), CELL_HEIGHT, data["name"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After Name: {0}, {1}".format(pdf.x, pdf.y))

    second_line_y = temp_y + (CELL_HEIGHT * 2)
    pdf.y = second_line_y

    # Line after name
    pdf.line(0, second_line_y, PAPER_WIDTH, second_line_y)

    temp_y = pdf.y
    third_line_y = temp_y + (CELL_HEIGHT * 2)

    num_of_lines = get_num_of_lines_in_multicell(pdf, data["use"], MAX_WIDTH)

    # To put the use in the middle of the box
    if num_of_lines == 1:
        pdf.y += 0.45

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)
    pdf.multi_cell(MAX_WIDTH, CELL_HEIGHT, data["use"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After use: {0}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after medicine usage
    pdf.line(0, third_line_y, PAPER_WIDTH, third_line_y)

    pdf.y = third_line_y
    
    fourth_line_y = third_line_y + CELL_HEIGHT

    pdf.set_xy(0.4, third_line_y)
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    title_width = pdf.get_string_width("Sehari")
    pdf.cell(title_width, CELL_HEIGHT, "Sehari")

    unit_width = pdf.get_string_width("Bungkus") + (MARGIN * 2)

    dose_pos_y = third_line_y + 0.15

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    pdf.set_xy(2.35, dose_pos_y)
    pdf.write_html(data["dose"])

    pdf.set_xy(4.3, third_line_y)
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(unit_width, CELL_HEIGHT, data["unit"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After dose: {0}, {1:.1f}".format(pdf.x, pdf.y))

    # Line after dose
    pdf.line(0, fourth_line_y, PAPER_WIDTH, fourth_line_y)

    pdf.y = fourth_line_y

    pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["consume_time"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("After consume time: {0}, {1:.1f}".format(pdf.x, pdf.y))
    
    # Line after when to eat the medicine
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    if data["must_finish"] is not None:
        pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
        pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["must_finish"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("Must finish: {0}, {1}".format(pdf.x, pdf.y))
    
    # Bottom line
    pdf.line(0, pdf.y, PAPER_WIDTH, pdf.y)

    file_name = path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today)
                                                 
    print(file_name)
    pdf.output(file_name)

    print_using_acrobat(file_name)
    # print_using_dialog(file_name)

    # pdf.output("trial.pdf")
    

if __name__ == "__main__":
    data = {
        "num": "123",
        "name": "Nicolai Christian Suhalim",
        # "use": "Antibiotik / Radang Tenggorokan",
        "use": "Antibiotik",
        "dose": "3 x 1",
        "consume_time": "Sebelum Makan",
        "must_finish": "Habiskan",
        "unit": "Tablet"
    }

    create_pdf_eticket(data)