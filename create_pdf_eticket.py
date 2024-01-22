from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os

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
    PAPER_HEIGHT = 6.5

    BOLD = "B"
    REGULAR = ""
    FONT_SIZE = 10
    BIGGER_FONT_SIZE = 14
    CELL_HEIGHT = 0.8
    MARGIN = 0.1
    MAX_WIDTH = PAPER_WIDTH - (MARGIN * 2)

    TITLE_BORDER = "LTB"
    BODY_BORDER = "TRB"

    today = date.strftime(date.today(), "%d-%m-%Y")

    parent_dir = "D:/"
    directory = "etiket_{0}".format(today)

    path = os.path.join(parent_dir, directory)

    try:
        os.mkdir(path)
    except:
        pass

    pdf = FPDF('P', 'cm', (PAPER_WIDTH, PAPER_HEIGHT))
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(False, MARGIN)


    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf")
    FONT_NAME = "Arial"


    # Add page
    pdf.add_page()
    
    TOP_COLUMN_WIDTH = (PAPER_WIDTH - (2 * MARGIN)) / 2

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)

    title_width = pdf.get_string_width("No.")
    num_col_width = title_width + 0.1

    pdf.cell(num_col_width, CELL_HEIGHT, "No.")

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)

    pdf.cell((TOP_COLUMN_WIDTH - num_col_width), CELL_HEIGHT, data["num"])

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    title_width = pdf.get_string_width("Tgl:")
    date_col_width = title_width + 0.1
    pdf.cell(date_col_width, CELL_HEIGHT, "Tgl:")

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    pdf.cell((TOP_COLUMN_WIDTH - date_col_width), CELL_HEIGHT, today, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    prev_x = pdf.x
    prev_y = pdf.y

    print("First row {0}, {1}".format(pdf.x, pdf.y))

    pdf.set_line_width(0.02)
    ######### FIRST LINE #############
    # pdf.line(0, 1, PAPER_WIDTH, 1)


    # pdf.line(pdf.x, pdf.y, (PAPER_WIDTH - MARGIN), pdf.y)
    pdf.line(0, 1, PAPER_WIDTH, 1)
    pdf.line(0, 2, PAPER_WIDTH, 2)
    pdf.line(0, 3, PAPER_WIDTH, 3)
    pdf.line(0, 4, PAPER_WIDTH, 4)
    pdf.line(0, 5, PAPER_WIDTH, 5)
    pdf.line(0, 6, PAPER_WIDTH, 6)
    
    pdf.line(1, 0, 1, PAPER_HEIGHT)
    pdf.line(2, 0, 2, PAPER_HEIGHT)
    pdf.line(3, 0, 3, PAPER_HEIGHT)
    pdf.line(4, 0, 4, PAPER_HEIGHT)
    pdf.line(5, 0, 5, PAPER_HEIGHT)

    pdf.y = 1.1 + 0.6

    title_width = pdf.get_string_width("Nama:")
    name_col_width = title_width + 0.1

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(name_col_width, None, "Nama:")

    num_of_lines_name = get_num_of_lines_in_multicell(pdf, data["name"], (MAX_WIDTH - name_col_width - 0.2))
    # print(num_of_lines_name)

    if num_of_lines_name > 1:
        pdf.y = 1.1
    else:
        pdf.y = 1.1 + 0.4
        
    pdf.x = name_col_width + MARGIN + 0.2

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    # pdf.cell((MAX_WIDTH - name_col_width), CELL_HEIGHT, data["name"], border=BODY_BORDER, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell((MAX_WIDTH - name_col_width - 0.2), CELL_HEIGHT, data["name"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.line(pdf.x, pdf.y, (PAPER_WIDTH - MARGIN), pdf.y)

    print("Second: {0}, {1}".format(pdf.x, pdf.y))

    pdf.y += 0.1

    pdf.set_font(FONT_NAME, REGULAR, BIGGER_FONT_SIZE)
    # pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["use"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(MAX_WIDTH, CELL_HEIGHT, data["use"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    print("Third: {0}, {1}".format(pdf.x, pdf.y))

    title_width = pdf.get_string_width("Sehari")
    a_day_width = title_width + 0.2
    pdf.cell(a_day_width, CELL_HEIGHT, "Sehari", border=TITLE_BORDER)

    unit_width = pdf.get_string_width("Bungkus") + 0.2

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    pdf.set_xy(2.5, (pdf.y + 0.15))
    pdf.write_html(data["dose"])


    pdf.set_xy(2.5, (pdf.y + 0.15))
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(unit_width, CELL_HEIGHT, data["unit"], border=BODY_BORDER, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # # consume_time = "Sebelum Makan"
    # pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["consume_time"], align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # # must_finish = None
    # if data["must_finish"] is not None:
    #     pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    #     pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["must_finish"], align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # # pdf.output("pdf_trial.pdf")

    # print(path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today))
    # pdf.output(path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today))
    pdf.output("trial.pdf")
    

if __name__ == "__main__":
    data = {
        "num": "123",
        "name": "Nicolai Christian Suhalim",
        "use": "Antibiotik / Radang Tenggorokan",
        "dose": "3 x 1",
        "consume_time": "Sebelum Makan",
        "must_finish": "Harus Habis",
        "unit": "Kapsul"
    }

    create_pdf_eticket(data)