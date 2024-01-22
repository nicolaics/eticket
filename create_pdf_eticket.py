from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import date
import os

def create_pdf_eticket(data):
    PAPER_WIDTH = 6
    PAPER_HEIGHT = 6.5

    # FONT_NAME = "helvetica"
    BOLD = "B"
    REGULAR = ""
    FONT_SIZE = 10
    BIGGER_FONT_SIZE = 14
    CELL_HEIGHT = 0.8
    MARGIN = 0.3
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

    pdf.set_line_width(0.02)
    pdf.line(pdf.x, pdf.y, (PAPER_WIDTH - MARGIN), pdf.y)

    start_name = 1.1 + 0.6

    pdf.y = start_name

    print(pdf.x, pdf.y)

    # title_width = pdf.get_string_width("Nama:")
    name_col_width = title_width + 0.1

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(name_col_width, None, "Nama:")

    pdf.x = name_col_width + MARGIN + 0.2
    pdf.y = 1.1

    pdf.set_font(FONT_NAME, BOLD, BIGGER_FONT_SIZE)
    # pdf.cell((MAX_WIDTH - name_col_width), CELL_HEIGHT, data["name"], border=BODY_BORDER, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell((MAX_WIDTH - name_col_width - 0.2), CELL_HEIGHT, data["name"], align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.line(pdf.x, pdf.y, (PAPER_WIDTH - MARGIN), pdf.y)

    print(pdf.x, pdf.y)

    # # use = "Antibiotik / Radang Tenggorokan"
    # pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    # pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["use"], border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # title_width = pdf.get_string_width("Sehari")
    # a_day_width = title_width + 0.2
    # pdf.cell(a_day_width, CELL_HEIGHT, "Sehari", border=TITLE_BORDER)

    # unit_width = pdf.get_string_width("Bungkus") + 0.2

    # pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    # pdf.set_xy(2.5, 2.8)
    # pdf.write_html(data["dose"])


    # pdf.set_xy(4.2, 2.6)
    # # unit = "Kapsul"
    # pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    # pdf.cell(unit_width, CELL_HEIGHT, data["unit"], border=BODY_BORDER, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
        "name": "Christian",
        "use": "Antibiotik / Radang Tenggorokan",
        "dose": "3 x 1",
        "consume_time": "Sebelum Makan",
        "must_finish": "Harus Habis",
        "unit": "Kapsul"
    }

    create_pdf_eticket(data)