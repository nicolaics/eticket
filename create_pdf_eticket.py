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
    FONT_SIZE = 8
    CELL_HEIGHT = 0.7
    MARGIN = 0.5
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

    TOP_COLUMN_WIDTH = 2.5

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)

    title_width = pdf.get_string_width("No.")
    num_col_width = title_width + 0.1

    pdf.cell(num_col_width, CELL_HEIGHT, "No.", border=TITLE_BORDER)

    # number = "222"
    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    pdf.cell((TOP_COLUMN_WIDTH - num_col_width), CELL_HEIGHT, data["num"], border=BODY_BORDER)

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)

    title_width = pdf.get_string_width("Tgl:")
    date_col_width = title_width + 0.1
    pdf.cell(date_col_width, CELL_HEIGHT, "Tgl:", border=TITLE_BORDER)

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    pdf.cell((TOP_COLUMN_WIDTH - date_col_width), CELL_HEIGHT, today, border=BODY_BORDER, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


    title_width = pdf.get_string_width("Nama:")
    name_col_width = title_width + 0.1

    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(name_col_width, CELL_HEIGHT, "Nama:", border=TITLE_BORDER)

    # name = "Nicolai Christian Suhalim"
    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    pdf.cell((MAX_WIDTH - name_col_width), CELL_HEIGHT, data["name"], border=BODY_BORDER, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # use = "Antibiotik / Radang Tenggorokan"
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["use"], border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    title_width = pdf.get_string_width("Sehari")
    a_day_width = title_width + 0.2
    pdf.cell(a_day_width, CELL_HEIGHT, "Sehari", border=TITLE_BORDER)

    unit_width = pdf.get_string_width("Bungkus") + 0.2


    # num_of_consume = "3"
    # dose = "1/12"
    # dose_split = dose.split('/')
    # dose = u"<b>{0} x <sup>{1}</sup>\u2044<sub>{2}</sub></b>".format(num_of_consume, dose_split[0], dose_split[1])

    # final_dose_str = u"<b>3 x <sup>1</sup>\u2044<sub>10</sub></b>"
    # final_dose_str = u"<b>3 x 1</b>"

    pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
    # pdf.cell((MAX_WIDTH - unit_width - a_day_width), CELL_HEIGHT, final_dose_str, align='C', border=1)

    pdf.set_xy(2.5, 2.8)
    pdf.write_html(data["dose"])


    pdf.set_xy(4.2, 2.6)
    # unit = "Kapsul"
    pdf.set_font(FONT_NAME, REGULAR, FONT_SIZE)
    pdf.cell(unit_width, CELL_HEIGHT, data["unit"], border=BODY_BORDER, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # consume_time = "Sebelum Makan"
    pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["consume_time"], align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # must_finish = None
    if data["must_finish"] is not None:
        pdf.set_font(FONT_NAME, BOLD, FONT_SIZE)
        pdf.cell(MAX_WIDTH, CELL_HEIGHT, data["must_finish"], align='C', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.output("pdf_trial.pdf")

    print(path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today))
    pdf.output(path + "/{0}_{1}_{2}.pdf".format(data["num"], data["name"], today))
    