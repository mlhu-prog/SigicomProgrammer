
def ReportGeneration(cache_main_dir, info):
    import os
    import shutil

    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, KeepTogether, Image, Paragraph, PageBreak, Spacer, Frame, Table, PageTemplate, BaseDocTemplate, TableStyle, ListFlowable, ListItem, tableofcontents
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import cm

    from basic_functions import load_json
    from basic_functions import month_danish


    from logger import get_logger

    ### Font, and other variables
    pdfmetrics.registerFont(TTFont("Verdana", "C:\\Windows\\Fonts\\Verdana.ttf"))
    pdfmetrics.registerFont(TTFont("Verdana-Bold", "C:\\Windows\\Fonts\\Verdanab.ttf"))
    pdfmetrics.registerFont(TTFont("TNR", "C:\\Windows\\Fonts\\times.ttf"))


    # Define the logo path and properties
    drive = "O:"
    files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
    logo_path = os.path.join(files_path,"Logo_no_background.png")
    watermark_path = os.path.join(files_path, "watermark.png")
    bullet_path = os.path.join(files_path,"markdown.png")

    logo_img = os.path.normpath(drive + os.sep + logo_path)
    watermark_img = os.path.normpath(drive + os.sep + watermark_path)
    bullet_img = os.path.normpath(drive + os.sep + bullet_path)
    files_path = os.path.normpath(drive + os.sep + files_path)

    danish_alphabet = "abcdefghijklmnopqrstuvwxyzæøå".upper()

    logo_width = 4 * cm  # Width of the logo
    logo_height = 1.5 * cm  # Height of the logo
    page_width, page_height = A4  # Page dimensions

    # Define RGB color (for example, COWI's specific shade of red)
    rgb_cowi_red = (240/255, 78/255, 35/255)
    rgb_cowi_blackTrans = (88/255, 89/255, 91/255)
    rgb_cowi_blackHead = (50/255, 50/255, 50/255)

    styles = getSampleStyleSheet()

    wrapped_style_text_above_tabel = ParagraphStyle(
        name='Wrapped',
        parent=styles['Normal'],
        fontSize=8,
        alignment=0,    # left alignment
    )

    underlined_style = ParagraphStyle(
        name='Underlined',
        parent=styles['Normal'],
        fontSize=10,
        alignment=0,
        us_lines=1  # Add underline
    )

    toc_title_style_indhold = styles['Heading1'].clone('title_style')
    toc_title_style_indhold.fontName = "Verdana" 
    toc_title_style_indhold.textColor = rgb_cowi_red
    toc_title_style_indhold.fontSize = 24
    toc_title_style_indhold.alignment = 0
    toc_title_style_indhold.spaceBefore = 150


    bilag_toc_title_style_indhold = styles['Heading1'].clone('bilag_title_style')
    bilag_toc_title_style_indhold.fontName = "Verdana" 
    bilag_toc_title_style_indhold.textColor = rgb_cowi_red
    bilag_toc_title_style_indhold.fontSize = 24
    bilag_toc_title_style_indhold.alignment = 0
    bilag_toc_title_style_indhold.spaceBefore = 40

    toc_appendix_style = styles['Heading1'].clone('appendix_style')
    toc_appendix_style.fontName = "Verdana" 
    toc_appendix_style.textColor = rgb_cowi_red
    toc_appendix_style.fontSize = 24
    toc_appendix_style.alignment = 0

    toc_title_style = ParagraphStyle(name='TOCTitle', fontSize=11, leading=16, spaceAfter=10, alignment=0, 
                                    textColor = rgb_cowi_red, spaceBefore=150, fontName="Verdana")
    toc_entry_style = ParagraphStyle(name='TOCEntry', fontSize=11, leading=16, alignment=0, firstLineIndent=0.5*cm)

    toc_style = styles['Normal'].clone('toc_style')
    toc_style.fontName = "Verdana"
    toc_style.fontSize = 11
    #toc_style.spaceAfter = 50
    toc_style.spaceBefore = 15


    heading1_style = styles["Heading1"].clone('heading1_style')
    heading1_style.fontName = "Verdana"
    heading1_style.fontSize = 16
    heading1_style.alignment = 0
    #heading1_style.firstLineIndent = 0.5 * cm 

    heading7_style = styles["Heading1"].clone('heading7_style')
    heading7_style.fontName = "Verdana"
    heading7_style.fontSize = 16
    heading7_style.alignment = 0
    #heading1_style.firstLineIndent = 0.5 * cm 

    heading1_num_style = styles["Heading1"].clone('heading1_num_style')
    heading1_num_style.fontName = "Verdana"
    heading1_num_style.fontSize = 16
    heading1_num_style.alignment = 0

    heading7_num_style = styles["Heading1"].clone('heading7_num_style')
    heading7_num_style.fontName = "Verdana"
    heading7_num_style.fontSize = 16
    heading7_num_style.alignment = 0



    tablestyle_heading = TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0,0), (0,-1), 'TOP')])  # Grid lines
                            #('GRID', (0, 0), (-1, -1), 0.5, colors.gray)])

    tablestyle_overskridelse = TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT')])  
                            #('VALIGN', (0, 0), (0, -1), 'TOP')])

    tablestyle_overskridelse_caption = TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),#])  
                            ('VALIGN', (0, 0), (0, -1), 'TOP')])

    tablestyle_overskridelse_bullet = TableStyle([
                            ('ALIGN', (0, 0), (0, -1), 'LEFT'),#])  
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'), 
                            ('TOPPADDING', (0, 0), (0, -1), 8)])
                            #('GRID', (0,0), (-1, -1), 0.5, colors.gray)])

    tablestyle_konklusion = TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Verdana-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ])


    # Define custom normal text style using Times New Roman
    normal_text_style = styles["Normal"].clone("normal_text_style")
    normal_text_style.fontName = "Times"
    normal_text_style.fontSize = 11
    normal_text_style.leading = 14
    normal_text_style.spaceAfter = 3
    normal_text_style.alignment = 0  # Left align

    # Define italic text style (Times New Roman Italic)
    italic_text_style = ParagraphStyle(name="ItalicStyle", fontName="Times-Italic", fontSize=11, leading=14)

    normal_text_style_bullet = styles["Normal"].clone('normal_text_style')
    normal_text_style_bullet.fontName = "TNR"
    normal_text_style_bullet.fontSize = 11
    normal_text_style_bullet.spaceAfter = 5
    normal_text_style_bullet.alignment = 0
    normal_text_style_bullet.firstLineIndent = 0.5 * cm 

    normal_text_style_overskridelser_bullet = styles["Normal"].clone('normal_text_style_overskridelser_bullet')
    normal_text_style_overskridelser_bullet.fontName = "TNR"
    normal_text_style_overskridelser_bullet.fontSize = 11
    normal_text_style_overskridelser_bullet.spaceAfter = 0
    normal_text_style_overskridelser_bullet.alignment = 0

    caption_text_style = styles["Normal"].clone('normal_text_style')
    caption_text_style.fontName = "Times-Italic"
    caption_text_style.fontSize = 9.5
    caption_text_style.spaceAfter = 6
    caption_text_style.alignment = 0

    table_text_style = styles["Normal"].clone('table_text_style')
    table_text_style.fontName = "Verdana"
    table_text_style.fontSize = 8

    note_text_style = styles["Normal"].clone('note_text_style')
    note_text_style.fontName = "Times"
    note_text_style.fontSize = 11
    note_text_style.leftIndent = -113.4 #-4.5*cm

    measure_point_header_style = styles["Normal"].clone('measure_point_header_style')
    measure_point_header_style.fontName = "Times-Bold"
    measure_point_header_style.fontSize = 11

    konklusion_measure_point_header_style = styles["Normal"].clone('konklusion_measure_point_header_style')
    konklusion_measure_point_header_style.fontName = "Verdana-Bold"
    konklusion_measure_point_header_style.fontSize = 8

    whitespace = "&nbsp;"*7

    logger = get_logger()
    def extract_year(date_submitted):
        if "-" in date_submitted:
            return date_submitted.split("-")[0]  # YYYY-MM-DD format
        elif "." in date_submitted:
            return date_submitted.split(".")[2]  # DD.MM.YYYY format
        else:
            raise ValueError("Unknown date format")
    def extract_month(date_submitted):
        if "-" in date_submitted:
            return month_danish(int(date_submitted.split("-")[1]))  # YYYY-MM-DD format
        elif "." in date_submitted:
            return month_danish(int(date_submitted.split(".")[1]))  # DD.MM.YYYY format
        else:
            raise ValueError("Unknown date format")
    def draw_wrapped_line(c, text, x_start, y_start, max_width):
        text_object = c.beginText(x_start, y_start)
        text_object.setFont('Verdana', 28)
        lines = []
        words = text.split()
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            if c.stringWidth(test_line, 'Verdana', 28) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word

        lines.append(line)  # Append the last line

        for line in lines:
            text_object.textLine(line)

        c.drawText(text_object)
        return y_start - 1.5 * cm * len(lines)  # Adjust the vertical position as needed for the next text

    def draw_wrapped_file_path(c, text, x_start, y_start, max_width):
        c.setFont('Verdana', 5.5)
        c.setFillColorRGB(*rgb_cowi_blackTrans)
        #c.drawString(3.15 * cm, 0.8 * cm, text)
        text_width = c.stringWidth(text, 'Verdana', 5.5)
        if text_width > max_width:
            parts = text.split("/")

            current_line = ""
            lines = []

            for part in parts:
                if c.stringWidth(f"{current_line}/{part}", 'Verdana', 5.5) <= max_width:
                    if current_line:
                        current_line += "/" + part
                    else:
                        current_line = part
                else:
                    lines.append(current_line)
                    current_line = part

            if current_line:
                lines.append(current_line)
        
            for line in lines:
                c.drawString(x_start, y_start, line)
                y_start -= 0.3 * cm
        else:
            c.drawString(x_start, y_start, text)
            
    def create_first_front_page(front_page_pdf, info):
        import shutil
        import tempfile
        out_file_pdf = os.path.join(cache_main_dir, "Temp", "First_Front_page.pdf")

        # Define margins
        left_margin = 2.5 * cm
        right_margin = 2.5 * cm
        top_margin = 2.5 * cm
        bottom_margin = 2.5 * cm
        page_width, page_height = A4
        max_text_width = page_width - left_margin - right_margin
        content_height_start = page_height - top_margin

        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_file_path = os.path.join(tmpdirname, 'temp_file.pdf')

            c = canvas.Canvas(temp_file_path, pagesize=A4)

            # Set up font (assuming Helvetica is close to the font used)
            c.setFont("Helvetica", 12)

            wat_img_width = 18.49 * cm
            wat_img_height = 20.43 * cm

            c.drawImage(watermark_img, page_width/2 - wat_img_width/2, bottom_margin + 1.1 * cm, width=wat_img_width, height=wat_img_height, mask='auto')

            new_y_position = content_height_start

            # Main title section
            c.setFont("Verdana", 9)
            c.setFillColor(colors.black)

            # Drawing the text with margins
            c.drawString(left_margin, new_y_position - 0 * cm, f"{extract_month(info['date_submitted']).capitalize()} {extract_year(info['date_submitted'])}".upper())
            c.drawString(left_margin, new_y_position - 0.5 * cm, f"{info['customer']}".upper())

            c.setFont("Verdana", 28)
            c.setFillColor(colors.black)
            c.drawString(left_margin, new_y_position - 1.8 * cm, "VIBRATIONSSOVERVÅGNING")

            road_city_text = f"{info['project_name']}".upper()
            new_y_position = draw_wrapped_line(c, road_city_text, left_margin, new_y_position - 3.0 * cm, max_text_width)

            # Subtitle
            c.setFont("Verdana", 9)
            c.drawString(left_margin, new_y_position + 1*cm, "MÅLERAPPORT")

            # Bottom right logo
            c.drawImage(logo_img, page_width - right_margin - logo_width + 1.4* cm, bottom_margin - 1.25 * cm, width=logo_width, height=logo_height, mask='auto')

            c.showPage()

            c.showPage()

            # Save the PDF
            c.save()

            # Ensure the destination directory exists
            if os.name == 'nt':
                out_file_pdf = f'\\\\?\\{os.path.abspath(out_file_pdf)}'

            os.makedirs(os.path.dirname(out_file_pdf), exist_ok=True)

            if os.path.exists(out_file_pdf):
                os.remove(out_file_pdf)

            # Use os.rename to move the temporary PDF to the final path and rename it
            shutil.copy(temp_file_path, out_file_pdf)
            os.remove(temp_file_path)

        return out_file_pdf
        
    def create_second_front_page(front_page_pdf, info):
        import shutil
        import tempfile

        # Define margins
        left_margin = 2.5 * cm
        right_margin = 2.5 * cm
        page_width, page_height = A4
        max_text_width = page_width - left_margin - right_margin
        out_file_pdf = os.path.join(cache_main_dir, "Temp","Second_Front_page.pdf")

        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_file_path = os.path.join(tmpdirname, 'temp_file.pdf')

            c = canvas.Canvas(temp_file_path, pagesize=A4)

            # Set up font (assuming Helvetica is close to the font used)
            c.setFont("Helvetica", 12)

            # Set up positions for text alignment
            x_position = page_width - logo_width + 0.1 * cm
            y_position = page_height -  logo_height - 2.44 * cm

            # Top right corner: company logo and address information
            c.drawImage(logo_img, page_width - 0.99 * cm - logo_width, page_height - 2.5 * cm, width=logo_width, height=logo_height, mask='auto')

            # Address text below logo
            c.setFont("Verdana", 5.5)
            c.setFillColorRGB(*rgb_cowi_red)
            text = "ADRESSE"
            c.drawRightString(x_position, y_position, text)
            text_width = pdfmetrics.stringWidth(text, "Verdana", 5.5)

            new_x_position = x_position+0.20*cm
            y_space = 0.40

            # Black larger text
            c.setFont("Verdana", 7)
            c.setFillColorRGB(*rgb_cowi_blackTrans)
            c.drawString(new_x_position, y_position, "COWI A/S")
            y_position -= y_space * cm
            c.drawString(new_x_position, y_position, "Visionsvej 53")
            y_position -= y_space * cm
            c.drawString(new_x_position, y_position, "9000 Aalborg")
            y_position -= y_space * cm
            c.drawString(new_x_position, y_position, "Danmark")
            # Red small text for contact labels
            c.setFont("Verdana", 5.5)
            c.setFillColorRGB(*rgb_cowi_red)
            y_position -= 0.75 * cm
            y_pos_org = y_position
            c.drawRightString(x_position, y_position, "TLF")
            y_position -= y_space * cm
            c.drawRightString(x_position, y_position, "FAX")
            y_position -= y_space * cm
            c.drawRightString(x_position, y_position, "WWW")

            # Black text for contact details
            c.setFont("Verdana", 7)
            y_position = y_pos_org
            c.setFillColorRGB(*rgb_cowi_blackTrans)
            c.drawString(new_x_position, y_position, "+45 56 40 00 00")
            y_position -= y_space * cm
            c.drawString(new_x_position, y_position, "+45 56 40 99 99")
            y_position -= y_space * cm
            c.drawString(new_x_position, y_position, "cowi.dk")

            # Main title section

            c.setFont("Verdana", 9)
            c.setFillColor(colors.black)
            
            c.drawString(2.5 * cm, page_height - 9 * cm, f"{extract_month(info['date_submitted']).capitalize()} {extract_year(info['date_submitted'])}".upper())
            
            c.drawString(2.5 * cm, page_height - 9.5 * cm, f"{info['customer']}".upper())
            c.setFont("Verdana", 28)
            c.setFillColor(colors.black)

            c.drawString(2.5 * cm, page_height - 10.8 * cm, "VIBRATIONSSOVERVÅGNING")

            road_city_text = f"{info['project_name']}".upper()
            new_y_position = draw_wrapped_line(c, road_city_text, 2.5 * cm, page_height - 12.0 * cm, max_text_width)
            #c.drawString(2.5 * cm, page_height - 12.0 * cm, f"{info['project_name']}".upper())

            # Subtitle
            c.setFont("Verdana", 9)
            c.drawString(2.5 * cm, new_y_position + 1.0 * cm, "MÅLERAPPORT")

            # Bottom left details
            c.setFont("Verdana", 5.5)
            c.setFillColorRGB(*rgb_cowi_red)
            y_pos = 4.4 * cm
            c.drawString(2.5 * cm, y_pos, "PROJEKTNR.")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "DOKUMENTNR.")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "VERSION")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "Udgivelsesdato")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "UDARBEJDET")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "KONTROLLERET")
            y_pos -= y_space * cm
            c.drawString(2.5 * cm, y_pos, "GODKENDT")

            c.setFont("Verdana", 7)
            c.setFillColor(colors.black)
            y_pos = 4.4 * cm
            c.drawString(4.5 * cm, y_pos, info["project_atr"])
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, info["documentnr"])
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, f"{float(info['versionsnr']):.1f}")
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, info["date_submitted"])
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, info["created"])
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, info["checked"])
            y_pos -= y_space * cm
            c.drawString(4.5 * cm, y_pos, info["approved"])
            y_pos -= y_space * cm

            # Bottom right logo
            # Bottom right logo (another instance, if needed)
            c.drawImage(logo_img,  page_width - 0.99 * cm - logo_width, 1.1 * cm, width=logo_width, height=logo_height, mask='auto')

            c.showPage()

            c.showPage()

            # Save the PDF
            c.save()
                    # Ensure the destination directory exists
            if os.name == 'nt':
                out_file_pdf = f'\\\\?\\{os.path.abspath(out_file_pdf)}'
            
            os.makedirs(os.path.dirname(out_file_pdf), exist_ok=True)
                
            if os.path.exists(out_file_pdf):
                os.remove(out_file_pdf)
            
            # Use os.rename to move the temporary PDF to the final path and rename it
            shutil.copy(temp_file_path, out_file_pdf)
            os.remove(temp_file_path)
        return out_file_pdf

    def create_main_document(cache_main_dir, info):
        import shutil
        from PySide6.QtWidgets import QMessageBox
        import markdown
        import string
        import tempfile

        out_file_pdf = os.path.join(cache_main_dir, "Temp","Main_page.pdf")

        sensor_dict = load_json(os.path.join(cache_main_dir,"API","project_sensor_dict_final.json"))
        trans_dict = load_json(os.path.join(cache_main_dir,"Results","trans_dict_final.json"))
        # Define the function to track pages for each section

        limits = [sensor_dict[adresse]["limit"] for adresse in sensor_dict]

        if all(limit == 3 for limit in limits):
            chap_5_limit = "vibrationsfølsomme"
        elif any(limit == 3 for limit in limits) and any(limit == 5 for limit in limits):
            chap_5_limit = "vibrationsfølsomme og normale"
        elif all(limit == 5 for limit in limits):
            chap_5_limit = "normale"
        else:
            chap_5_limit = "ukendt"

        class MyDocTemplate(BaseDocTemplate):
            def __init__(self, filename, info, **kw):

                self.allowSplitting = 0
                BaseDocTemplate.__init__(self, filename, **kw)
                
                #self.chapter_counter = 1  # Start the chapter counter at 1
                def add_header_odd(canvas, doc):
                    # Save the state of the canvas
                    canvas.saveState()
                    # First line (Bold, FontSize 12)
                    canvas.drawImage(logo_img,  page_width - 2.25 * cm - 0.66*cm, page_height - 1.75 * cm, width=0.66*cm, height=0.22*cm, mask='auto')
                    # Second line (Normal, FontSize 10)
                    header_line2 = f"VIBRATIONSOVERVÅGNING, {info['project_name']}".upper()
                    canvas.setFont('Verdana', 7)
                    canvas.setFillColorRGB(*rgb_cowi_blackHead)
                    canvas.drawRightString(page_width - 2.25 * cm, page_height - 1.99 * cm, header_line2)  # Adjust the Y position for the second line

                    # Add page number at the bottom
                    page_number_text = f"{doc.page + 4}"
                    canvas.setFont('Verdana', 7)
                    canvas.setFillColorRGB(*rgb_cowi_blackHead)
                    canvas.drawRightString(page_width - 1.54 * cm, page_height - 1.99 * cm, page_number_text)


                    header_line3 = info["onedrive_link"]
                    #canvas.setFont('Verdana', 5.5)
                    #canvas.setFillColorRGB(*rgb_cowi_blackTrans)
                    #canvas.drawString(3.15 * cm, 0.8 * cm, header_line3)  # Adjust the Y position for the second line
                    
                    draw_wrapped_file_path(canvas, header_line3, 3.15 * cm, 0.8 * cm, (doc.width))

                    #add_link(canvas, doc)

                    canvas.restoreState()

                def add_header_even(canvas, doc):
                    # Save the state of the canvas
                    canvas.saveState()
                    # First line (Bold, FontSize 12)
                    canvas.drawImage(logo_img,  2.25 * cm, page_height - 1.75 * cm, width=0.66*cm, height=0.22*cm, mask='auto')
                    # Second line (Normal, FontSize 10)
                    header_line2 = f"VIBRATIONSOVERVÅGNING, {info['project_name']}".upper()
                    canvas.setFont('Verdana', 7)
                    canvas.setFillColorRGB(*rgb_cowi_blackHead)
                    canvas.drawString(2.25 * cm, page_height - 1.99 * cm, header_line2)  # Adjust the Y position for the second line

                    # Add page number
                    page_number_text = f"{doc.page + 4}"
                    canvas.setFont('Verdana', 7)
                    canvas.setFillColorRGB(*rgb_cowi_blackHead)
                    canvas.drawString(1.54 * cm, page_height - 1.99 * cm, page_number_text)

                    header_line3 = info["onedrive_link"]
                    #canvas.setFont('Verdana', 5.5)
                    #canvas.setFillColorRGB(*rgb_cowi_blackTrans)
                    #canvas.drawString(2.15 * cm, 0.8 * cm, header_line3)  # Adjust the Y position for the second line
                    
                    draw_wrapped_file_path(canvas, header_line3, 2.15 * cm, 0.8 * cm, (doc.width))

                    #add_link(canvas, doc)

                    canvas.restoreState()
                # Define custom functions for adding headers/footers based on page type
                def add_odd_even_page(canvas, doc):
                    if doc.page % 2 == 1:
                        doc.pageTemplate = doc.pageTemplates[0]
                        add_header_odd(canvas, doc)
                    else:
                        doc.pageTemplate = doc.pageTemplates[1]
                        add_header_even(canvas, doc)
                # Add the PageTemplate to the document

                odd_page_template = PageTemplate(id='odd_page', frames=odd_page_frame, onPage=add_odd_even_page)
                even_page_template = PageTemplate(id='even_page', frames=even_page_frame, onPage=add_odd_even_page)


                self.addPageTemplates([odd_page_template, even_page_template])

            def afterFlowable(self, flowable):
                "Registers TOC entries."
                if flowable.__class__.__name__ == 'Paragraph':
                    text = flowable.getPlainText()
                    style = flowable.style.name
                    if style == 'heading1_style':
                        self.notify('TOCEntry', (0, text, self.page+4))
                    if style == 'Heading2':
                        self.notify('TOCEntry', (1, text, self.page+4))

        with tempfile.TemporaryDirectory() as tmpdirname:

            pdf = BaseDocTemplate("temp.pdf", pagesize=A4, showBoundary=1)
            pdf.leftMargin = 155.95 #5.5 * cm #155.905
            pdf.rightMargin = 42.55 #1.5 * cm #42.52
            pdf.topMargin = 85.05 #3 * cm #80
            pdf.bottomMargin = 56.7 #2 * cm #56.693
            gutter = 28.35 #1 * cm
            temp_file_path = os.path.join(tmpdirname, 'temp_file.pdf')
            #frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')

            # Define frames with different margins
            odd_page_frame = Frame(
                pdf.leftMargin + gutter, pdf.bottomMargin,
                pdf.pagesize[0] - pdf.rightMargin - pdf.leftMargin - gutter, pdf.pagesize[1] - pdf.topMargin - pdf.bottomMargin,
                id='odd_frame'
            )

            even_page_frame = Frame(
                pdf.leftMargin, pdf.bottomMargin,  # Add some offset to the left margin for even pages
                pdf.pagesize[0] - pdf.rightMargin - pdf.leftMargin - gutter, pdf.pagesize[1] - pdf.topMargin - pdf.bottomMargin,
                id='even_frame'
            )
            pdf = MyDocTemplate(temp_file_path, info)
            
            # Initialize ToC
            toc = TableOfContents()
            toc.levelStyles = [
                ParagraphStyle(name='TOCHeading1', fontSize=11, leading=14, fontName="Verdana", 
                                spaceBefore=10, spaceAfter=50),
                ParagraphStyle(name='TOCHeading2', fontSize=15, leading=12, leftIndent=40),
            ]

            
            ### Table of Content ###   
            #toc = TableOfContents()
            #toc.levelStyles = [toc_entry_style]  # Set the styles for each level in the ToC

            toc_content = [Spacer(1, 5), Paragraph("INDHOLD", toc_title_style_indhold), Spacer(1, 4)]
            
            toc_content.append(Spacer(0, 3))

            bilag_toc_content = [Paragraph("BILAG", bilag_toc_title_style_indhold), Spacer(1, 4)]

            for i, (adresse, details) in enumerate(trans_dict.items()):
                bilag_toc_content.append(Spacer(0, 5))
                bilag_toc_content.append(Paragraph(f"Bilag {danish_alphabet[i]}{whitespace}{adresse}", toc_style))

            # Define the sections
            ### Kapitel 1 Indledning ###
            indledning_text_path = os.path.join(cache_main_dir,"Rapport","Tekst","Indledning.md")
            with open(indledning_text_path, 'r', encoding='utf-8') as file:
                indledning_text = file.read()
            
            indledning_text = indledning_text.replace('\n', '<br />')

            # Example of adding a section to ToC dynamically
            ind_content = []
            ind_content.append(Spacer(0, 170))
            ind_title = Paragraph(f"1{whitespace}Indledning", heading1_style)#[[Paragraph("1", heading1_num_style), Paragraph("Indledning", heading1_style)]]
            #t = Table(ind_title, colWidths=[1*cm, 12*cm], hAlign='LEFT')
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            ind_content.append(ind_title)

            # Track this section in ToC (1 for main section)
            #add_toc_entry(toc, 1, "Indledning", pdf.page)  # Use current page
            #ind_content.append(Spacer(0, 3))
            ind_content.append(Paragraph(indledning_text,normal_text_style))

            ### Kapitel 2 Anlægsarbejde ###
            arbejde_text_path = os.path.join(cache_main_dir,"Rapport","Tekst","Anlægsarbejde.md")
            with open(arbejde_text_path, 'r', encoding='utf-8') as file:
                arbejde_text = file.read()
            
            #arbejde_text = arbejde_text.replace('\n', '<br />')
            
            arbejde_text = markdown.markdown(arbejde_text)


            arb_content = []
            arb_content.append(Spacer(0, 5))
            arb_title = Paragraph(f"2{whitespace}Anlægsarbejde", heading1_style)
            #arb_title = [[Paragraph("2", heading1_num_style), Paragraph("Anlægsarbejde",heading1_style)]]
            #t = Table(arb_title, colWidths=[1*cm, 12*cm])
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            arb_content.append(arb_title)

            # Process lines in arbejde_text with custom bullet style
            img_bullet = Image(bullet_img)
            img_bullet.drawWidth = 0.139 * cm 
            img_bullet.drawHeight = 0.15 * cm
            idx = 0 
            for line in arbejde_text.splitlines():
                if (line.startswith("<li>") or line.startswith("- ")) and idx == 0:  # Check for bullet points (assuming Markdown style with "-")
                    indexer = 4 if line.startswith("<li>") else 2
                    arb_bullet = [[img_bullet, Paragraph(line[indexer:],normal_text_style_bullet)]]
                    idx =+1
                elif (line.startswith("<li>") or line.startswith("- ")) and idx != 0:
                    indexer = 4 if line.startswith("<li>") else 2
                    arb_bullet.append([img_bullet, Paragraph(line[indexer:], normal_text_style_bullet)])
                else:
                    arb_content.append(Paragraph(line, normal_text_style))

            t = Table(arb_bullet, colWidths=[0.3 * cm, 16 * cm])
            t.setStyle(tablestyle_overskridelse)
            t.hAlign = 'LEFT'
            arb_content.append(t)

            ### Kapitel 3 Måleopstilling ###
            ## Oversigtsfoto ##
            mål_text1_path = os.path.join(files_path,"Tekst","Måleopstilling_1.md")
            with open(mål_text1_path, 'r', encoding='utf-8') as file:
                mål_text1 = file.read()

            mål_text2_path = os.path.join(files_path,"Tekst","Måleopstilling_2.md")
            with open(mål_text2_path, 'r', encoding='utf-8') as file:
                mål_text2 = file.read()

            mål_textCap_path = os.path.join(files_path,"Tekst","Måleopstilling_caption.md")
            with open(mål_textCap_path, 'r', encoding='utf-8') as file:
                mål_textCap = file.read()

            foto_list = [foto for foto in os.listdir(os.path.join(cache_main_dir,"Rapport", "Figurer","Oversigtsfoto")) if foto.lower().__contains__("jpg")]

            mål_content = []
            mål_title = Paragraph(f"3{whitespace}Måleopstilling", heading1_style)
            #mål_title = [[Paragraph("3", heading1_num_style), Paragraph("Måleopstilling",heading1_style)]]
            #t = Table(mål_title, colWidths=[1*cm, 12*cm])
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            mål_content.append(mål_title)
            #ind_content.append(Spacer(0, 3))
            mål_text1 = mål_text1 if len(foto_list) == 1 else mål_text1.replace("figur","figurer")
            mål_content.append(Paragraph(mål_text1,normal_text_style))
            mål_content.append(Spacer(0, 3))
            fig_num = 1
            for idx, foto in enumerate(foto_list):
                img_path = os.path.join(cache_main_dir, "Rapport", "Figurer", "Oversigtsfoto", foto)
                
                # Load the image
                img = Image(img_path)
                
                # Get the current image dimensions (width and height)
                img_width, img_height = img.imageWidth, img.imageHeight
                
                aspect_ratio = img_width/img_height

                img.drawWidth = odd_page_frame._width - 10
                img.drawHeight = img.drawWidth/aspect_ratio

                img.imageWidth = img.drawWidth
                img.imageHeight = img.drawHeight
                
                # Check if the height exceeds the frame height and adjust if necessary
                if img.imageHeight > odd_page_frame._height:
                    img.drawHeight = odd_page_frame._height
                    img.drawWidth = img.imageHeight * aspect_ratio

                mål_content.append(img)
        
                # Add a caption immediately below the image

                cap_text = [[Paragraph(f"Figur {fig_num}", caption_text_style), 
                            Paragraph(mål_textCap.splitlines()[0], caption_text_style), 
                            Paragraph(mål_textCap.splitlines()[1], caption_text_style)]]
                cap_tab = Table(cap_text, colWidths=[1.5*cm, 5.5*cm, 6.5*cm])
                cap_tab.hAlign = 'LEFT'
                cap_tab.setStyle(tablestyle_heading)
                mål_content.append(cap_tab)
                #caption = Paragraph(caption_text, caption_text_style)
                #mål_content.append(caption)
                mål_content.append(Spacer(0, 6))

                fig_num += 1
            
            mål_content.append(Paragraph(mål_text2,normal_text_style))
            
            ## Instrumenteringstabel ##
            def build_table_data(sensor_dict):
                from datetime import datetime
                #date_from = 
                # Header row
                data = [
                        [Paragraph("Målepunkt", table_text_style), Paragraph("Måle-<br />instrument",table_text_style), 
                        Paragraph("Kanal/<br />Serienummer", table_text_style),
                        Paragraph("Måleretning", table_text_style), Paragraph("Måleperiode",table_text_style)]
                        ]
                
                # Populate rows based on sensor_dict
                used_adresses = set()
                mp_counter = 1
                for i, (adresse, details) in enumerate(sensor_dict.items(), start=1):
                    base_key = adresse.split("_")[0]
                    
                    if base_key in used_adresses:
                        name = ""
                        mp = ""
                    else:
                        name = adresse
                        mp = f"Målepunkt {mp_counter}"
                        used_adresses.add(base_key)
                        mp_counter += 1

                    date_from = datetime.strptime(details["date_from"],"%Y-%m-%d %H:%M").strftime("%d-%m-%Y")
                    date_to = datetime.strptime(details["date_to"],"%Y-%m-%d %H:%M").strftime("%d-%m-%Y")
                    # Row for "Målepunkt"
                    if sensor_dict[adresse]["logger"] == "V12":
                        sens_id1 = details['sensor_id']
                        sens_id2 = str(int(float(details['sensor_id']) + 1))
                        sens_id3 = int(float(details['sensor_id']) + 2)
                    else:
                        sens_id1 = ""
                        sens_id2 = details['sensor_id']
                        sens_id3 = ""

                    data.append([Paragraph(mp,table_text_style), "", Paragraph(f"{sens_id1}", table_text_style), Paragraph("Lodret",table_text_style), Paragraph(f"{date_from} -",table_text_style)])
                    # Row for "Adresse"
                    data.append([
                        Paragraph(name, table_text_style), 
                        Paragraph(details['logger'],table_text_style),
                        Paragraph(f"{sens_id2}",table_text_style), 
                        Paragraph("Vandret Parallel",table_text_style), 
                        Paragraph(f"{date_to}",table_text_style)
                    ])
                    # Sub-rows for "Måleretning" and dates
                    data.append(["", "", Paragraph(f"{sens_id3}", table_text_style), Paragraph("Vandret Vinkelret",table_text_style), ""])

                return data
            
            mål_content.append(Spacer(0,6))
            instr_text = [[Paragraph(f"Tabel 1", caption_text_style), 
                    Paragraph("Instrumentering", caption_text_style)]]
            instr_tab = Table(instr_text, colWidths=[1.5*cm, 5.5*cm])
            instr_tab.hAlign = 'LEFT'
            instr_tab.setStyle(tablestyle_heading)
            mål_content.append(instr_tab)
            
            data = build_table_data(sensor_dict)
            table = Table(data, colWidths=[3.4*cm, 2*cm, 2.3*cm, 3.0*cm, 2.6*cm])
            table.hAlign = 'LEFT'
            #table._argW[0] = 1.56 * cm

            # Add styling
            style_instr_table = TableStyle([
                ('GRID', (0, 0), (-1, 0), 0.5, colors.black),  # Gridlines
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ])

            num_rows = len(data)
            for i in range(1, num_rows, 3):
                # Calculate the start and end row indices for the 3-row block
                if data[i][0].text == "":
                    style_instr_table.add('SPAN', (0, i-1), (0,i+1))
                start_row = i
                end_row = min(i + 2, num_rows - 1)  # Ensure it doesn't go beyond the table
                style_instr_table.add('BOX', (0, start_row), (-1, end_row), 1, colors.black)
                style_instr_table.add('BOX', (0, start_row), (-1, end_row), 1, colors.black)
            num_columns = len(data[0])
            for col in range(1, num_columns):  # Start from 1 to avoid a line on the leftmost edge
                style_instr_table.add('LINEBEFORE', (col, 0), (col, -1), 0.5, colors.black)

            # Optionally, add an outline box around the whole table
            style_instr_table.add('BOX', (0, 0), (-1, -1), 1, colors.black)

            table.setStyle(style_instr_table)

            mål_content.append(table)

            ### Kapitel 4 Målekonditioner ###
            målKon_file = os.path.join(cache_main_dir, "Rapport", "Tekst", "Målekonditioner.md")
            
            if not os.path.exists(målKon_file):
                målKon_file = os.path.join(files_path,"Tekst","Målekonditioner.md")

            with open(målKon_file, 'r', encoding='utf-8') as file:
                målKon_text = file.read()        

            målKon_text = målKon_text.replace('\n', '<br />')

            målKon_text = markdown.markdown(målKon_text)
            målKon_text = målKon_text.replace('<em>', '<i>').replace('</em>', '</i>')


            målKon_content = []
            målKon_content.append(Spacer(0, 5))
            målKon_title = Paragraph(f"4{whitespace}Målekonditioner", heading1_style)
            #målKon_title = [[Paragraph("4", heading1_num_style), Paragraph("Målekonditioner",heading1_style)]]
            #t = Table(målKon_title, colWidths=[1*cm, 12*cm], hAlign='LEFT')
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            målKon_content.append(målKon_title)
            #ind_content.append(Spacer(0, 3))
            målKon_content.append(Paragraph(målKon_text,normal_text_style))

            ### Kapitel 5 Grænseværdi for bygningsskader ###
            GrVr_text_path_1 = os.path.join(cache_main_dir, "Rapport", "Tekst", "GrænseværdiForBygningskader.md")
            GrVr_text_path_2 = os.path.join(cache_main_dir, "Rapport", "Tekst", "GrænseværdiForBygningskader_2.md")

            GrVr_text_path_1_main = os.path.join(files_path,"Tekst","GrænseværdiForBygningskader.md")
            GrVr_text_path_2_main = os.path.join(files_path,"Tekst","GrænseværdiForBygningskader_2.md")

            if os.path.exists(GrVr_text_path_1):
                with open(GrVr_text_path_1, 'r', encoding='utf-8') as file:
                    GrVr_text1 = file.read()    
            else:
                with open(GrVr_text_path_1_main, 'r', encoding='utf-8') as file:
                    GrVr_text1 = file.read()    

            if os.path.exists(GrVr_text_path_2):
                with open(GrVr_text_path_2, 'r', encoding='utf-8') as file:
                    GrVr_text2 = file.read()    
            else:
                with open(GrVr_text_path_2_main, 'r', encoding='utf-8') as file:
                    GrVr_text2 = file.read()    

                    GrVr_text2 = GrVr_text2.replace("VIB_ELLER_NORMAL", chap_5_limit)

            GrVr_text1 = GrVr_text1.replace('\n', '<br />')

            GrVr_text2 = GrVr_text2.replace('\n', '<br />')

            GrVr_text1 = markdown.markdown(GrVr_text1)
            GrVr_text2 = markdown.markdown(GrVr_text2)

            GrVr_text1 = GrVr_text1.replace('<em>', '<i>').replace('</em>', '</i>')
            GrVr_text2 = GrVr_text2.replace('<em>', '<i>').replace('</em>', '</i>')


            GrVr_content = []
            GrVr_content.append(Spacer(0, 5))
            GrVr_title = Paragraph(f"5{whitespace}Grænseværdi for bygningsskader", heading1_style)
            #GrVr_title = [[Paragraph("5", heading1_num_style), Paragraph("Grænseværdi for bygningsskader",heading1_style)]]
            # = Table(GrVr_title, colWidths=[1*cm, 12*cm], hAlign='LEFT')
            #.setStyle(tablestyle_heading)
            #.hAlign = 'LEFT'
            GrVr_content.append(GrVr_title)
            note_text = "DIN 4150"
            GrVr_content.append(Paragraph(note_text, note_text_style))
            GrVr_content.append(Spacer(0,-14))
            GrVr_content.append(Paragraph(GrVr_text1, normal_text_style))
            img_path = os.path.join(files_path, "Grænseværdier.png")
            
            # Load the image
            img = Image(img_path)
            
            # Get the current image dimensions (width and height)
            img_width, img_height = img.imageWidth, img.imageHeight
            
            aspect_ratio = img_width/img_height
            
            img.drawWidth = odd_page_frame._width - 10
            img.drawHeight = img.drawWidth/aspect_ratio

            img.imageWidth = img.drawWidth
            img.imageHeight = img.drawHeight
            
            # Check if the height exceeds the frame height and adjust if necessary
            if img.imageHeight > odd_page_frame._height:
                img.drawHeight = odd_page_frame._height
                img.drawWidth = img.imageHeight * aspect_ratio

            GrVr_content.append(img)

            # Add a caption immediately below the image
            
            cap_text = [[Paragraph(f"Figur {fig_num}", caption_text_style), 
                        Paragraph("Grænseværdier jf. DIN 4150-3", caption_text_style)]]
            cap_tab = Table(cap_text, colWidths=[1.5*cm, 5.5*cm])
            cap_tab.hAlign = 'LEFT'
            cap_tab.setStyle(tablestyle_heading)
            GrVr_content.append(cap_tab)
            GrVr_content.append(Spacer(0,3))
            GrVr_content.append(Paragraph(GrVr_text2,normal_text_style))
            fig_num += 1
            
            ### Kapitel 6 - Måleresultater ### 
            målRes_file = os.path.join(cache_main_dir, "Rapport", "Tekst", "Måleresultater_start.md")
            
            if not os.path.exists(målRes_file):
                målRes_file = os.path.join(files_path,"Tekst","Måleresultater_start.md")

            with open(målRes_file, 'r', encoding='utf-8') as file:
                målRes_text = file.read()     

            målRes_text = målRes_text.replace('\n', '<br />')

            målRes_text = markdown.markdown(målRes_text)
            målRes_text = målRes_text.replace('<em>', '<i>').replace('</em>', '</i>')


            if "BILAG_START-BILAG_SLUT" in målRes_text:
                if len(trans_dict) == 1:
                    målRes_text = målRes_text.replace("BILAG_START-BILAG_SLUT", f"{string.ascii_uppercase[0]}")
                else:
                    målRes_text = målRes_text.replace("BILAG_START", f"{string.ascii_uppercase[0]}").replace("BILAG_SLUT",f"{string.ascii_uppercase[len(trans_dict)-1]}")

            målRes_content = []
            målRes_content.append(Spacer(0, 5))
            målRes_title = Paragraph(f"6{whitespace}Måleresultater", heading1_style)
            #målRes_title = [[Paragraph("6", heading1_num_style), Paragraph("Måleresultater",heading1_style)]]
            #t = Table(målRes_title, colWidths=[1*cm, 12*cm], hAlign='LEFT')
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            målRes_content.append(målRes_title)
            #ind_content.append(Spacer(0, 3))
            målRes_content.append(Paragraph(målRes_text,normal_text_style))

            målRes_content.append(Spacer(0, 6))

            for i, (adresse, details) in enumerate(trans_dict.items()):
                text_final_path = os.path.join(cache_main_dir, "Rapport", "Tekst", f"{adresse}")
                fig_final_path = os.path.join(cache_main_dir, "Rapport", "Figurer", f"{adresse}")
                limit = sensor_dict[adresse]["limit"]
                logger = sensor_dict[adresse]["logger"]
                Reel = details['Reel']
                Slag = details['Slag']
                Arbe = details['Arbe']
                heading = Paragraph(f"Målepunkt {i+1}, {adresse}", measure_point_header_style)

                if all(val == 0 for val in [Reel, Slag, Arbe]):
                    text_final_file = os.path.join(text_final_path,"text_1.md")

                    with open(text_final_file, 'r', encoding='utf-8') as file:
                        text = file.read()
                    
                    text = text.replace('\n', '<br />')

                    målRes_content.append(KeepTogether([heading, Spacer(0,3), Paragraph(text,normal_text_style), Spacer(0,14)]))
                    #målRes_content.append(Spacer(0,3))

                elif Slag != 0 and Reel == 0 and Arbe == 0:
                    text_final_file = os.path.join(text_final_path,"text_1.md")

                    with open(text_final_file, 'r', encoding='utf-8') as file:
                        text = file.read()
                    
                    text = text.replace('\n', '<br />')

                    målRes_content.append(KeepTogether([heading, Spacer(0,3), Paragraph(text,normal_text_style), Spacer(0,14)]))
                    #målRes_content.append(Spacer(0, 1))

                elif Reel != 0 or Arbe != 0:
                    text_final_file = os.path.join(text_final_path,"text_1.md")

                    with open(text_final_file, 'r', encoding='utf-8') as file:
                        text = file.read()
                    
                    text = text.replace('\n', '<br />')

                    målRes_content.append(KeepTogether([heading, Spacer(0,3), Paragraph(text,normal_text_style)]))
                    #målRes_content.append(Spacer(0, 1))
                    img_path = os.path.join(fig_final_path, "Transienter_limit_3.jpg")
                    
                    # Load the image
                    img = Image(img_path)
                    
                    # Get the current image dimensions (width and height)
                    img_width, img_height = img.imageWidth, img.imageHeight
                    
                    aspect_ratio = img_width/img_height
                    
                    img.drawWidth = odd_page_frame._width - 10
                    img.drawHeight = img.drawWidth/aspect_ratio

                    img.imageWidth = img.drawWidth
                    img.imageHeight = img.drawHeight
                    
                    # Check if the height exceeds the frame height and adjust if necessary
                    if img.imageHeight > odd_page_frame._height:
                        img.drawHeight = odd_page_frame._height
                        img.drawWidth = img.imageHeight * aspect_ratio
                      
                    cap_path_text = os.path.join(files_path, "Tekst", "Måleresultater", f"{logger}", f"Overskridelser_caption_{limit}.md")
                    with open(cap_path_text, 'r', encoding='utf-8') as file:
                        text_cap = file.read()

                
                    cap_text = [[Paragraph(f"Figur {fig_num}", caption_text_style), 
                                Paragraph(text_cap, caption_text_style)]]
                    
                    cap_tab = Table(cap_text, colWidths=[1.5*cm, 10*cm])
                    cap_tab.hAlign = 'LEFT'
                    cap_tab.setStyle(tablestyle_overskridelse_caption)
                    målRes_content.append(KeepTogether([img, cap_tab]))
                    fig_num += 1


                    text_final_file = os.path.join(text_final_path,"text_2.md")

                    with open(text_final_file, 'r', encoding='utf-8') as file:
                        text = file.read()
                    
                    text = markdown.markdown(text)

                    img_bullet = Image(bullet_img)
                    img_bullet.drawWidth = 0.139 * cm 
                    img_bullet.drawHeight = 0.15 * cm
                    idx = 0 
                    for line in text.splitlines():
                        if line.startswith("- ") and idx == 0:  # Check for bullet points (assuming Markdown style with "-")
                            trans_bullet = [[img_bullet, Paragraph(line[2:],normal_text_style_overskridelser_bullet)]]
                            idx =+1
                        elif line.startswith("- ") and idx != 0:
                            trans_bullet.append([img_bullet, Paragraph(line[2:], normal_text_style_overskridelser_bullet)])
                        else:
                            målRes_content.append(Paragraph(line, normal_text_style))
                            målRes_content.append(Spacer(0,6))

                    t = Table(trans_bullet, colWidths=[0.8 * cm, 11.6 * cm])
                    t.setStyle(tablestyle_overskridelse_bullet)
                    t.hAlign = 'LEFT'
                    målRes_content.append(t)
                    målRes_content.append(Spacer(0,6))

                    text_final_file = os.path.join(text_final_path,"text_3.md")

                    if os.path.exists(text_final_file):
                        with open(text_final_file, 'r', encoding='utf-8') as file:
                            text = file.read()
                        
                        text = markdown.markdown(text)

                        img_bullet = Image(bullet_img)
                        img_bullet.drawWidth = 0.139 * cm 
                        img_bullet.drawHeight = 0.15 * cm
                        idx = 0 
                        trans_bullet = None
                        for line in text.splitlines():
                            if line.startswith("- ") and idx == 0:  # Check for bullet points (assuming Markdown style with "-")
                                trans_bullet = [[img_bullet, Paragraph(line[2:],normal_text_style_overskridelser_bullet)]]
                                idx =+1
                            elif line.startswith("- ") and idx != 0:
                                trans_bullet.append([img_bullet, Paragraph(line[2:], normal_text_style_overskridelser_bullet)])
                            else:
                                målRes_content.append(Paragraph(line, normal_text_style))
                                
                        if trans_bullet:
                            t = Table(trans_bullet, colWidths=[0.8 * cm, 11.6 * cm])
                            t.setStyle(tablestyle_overskridelse_bullet)
                            t.hAlign = 'LEFT'
                            målRes_content.append(t)
                        målRes_content.append(Spacer(0,14))

            ### Kapitel 7 - Konklusion ###
            
            with open(indledning_text_path, 'r', encoding='utf-8') as file:
                indledning_text = file.read()

            # Example of adding a section to ToC dynamically
            text = indledning_text.split("\n\n")[0]

            kon_content = []

            kon_title = Paragraph(f"7{whitespace}Konklusion", heading1_style)#[[Paragraph("1", heading1_num_style), Paragraph("Indledning", heading1_style)]]
            #t = Table(ind_title, colWidths=[1*cm, 12*cm], hAlign='LEFT')
            #t.setStyle(tablestyle_heading)
            #t.hAlign = 'LEFT'
            kon_content.append(kon_title)

            # Track this section in ToC (1 for main section)
            #add_toc_entry(toc, 1, "Indledning", pdf.page)  # Use current page
            #ind_content.append(Spacer(0, 3))
            kon_content.append(Paragraph(text,normal_text_style))
            kon_content.append(Spacer(0,6))

            Slag = 0
            Reel = 0

            for adresse, detail in trans_dict.items():
                Slag = Slag + detail["Slag"]
                Reel = Reel + detail["Reel"] + detail["Arbe"]
            
            text_path = os.path.join(cache_main_dir,"Rapport","Tekst","Konklusion_1.md")
            with open(text_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            kon_content.append(Paragraph(text, normal_text_style))

            kon_content.append(Spacer(0,6))

            if Reel != 0:
                ## Creating table
                data = [["Målepunkt", "Tidspunkt for overskridelse"]]

                with open(os.path.join(cache_main_dir,"Rapport","Tekst","Konklusion_caption.md"), 'r', encoding='utf-8') as file:
                    text = file.read()


                kon_cap_text = [[Paragraph(f"Tabel 2", caption_text_style), 
                        Paragraph(text, caption_text_style)]]
                
                kon_tab = Table(kon_cap_text, colWidths=[1.5*cm, 11.5*cm])
                kon_tab.hAlign = 'LEFT'
                kon_tab.setStyle(tablestyle_heading)
                kon_content.append(kon_tab)


                for adresse, details in trans_dict.items():
                    result_path = os.path.join(cache_main_dir,"Rapport","Tekst",adresse)
                    text_bullet_path = os.path.join(result_path,"text_2.md")
                    bullet_points = []
                    if os.path.exists(text_bullet_path):
                        with open(text_bullet_path, 'r', encoding='utf-8') as file:
                            for line in file:
                                line = line.strip()
                                if line.startswith("- "):
                                    text = line.split("Maksimal")[0]
                                    bullet_points.append(text[2:])
                    
                        bullet_text = "<br />".join(bullet_points)
                        data.append([Paragraph(f"{adresse}",table_text_style), Paragraph(bullet_text, table_text_style)])
                
                table = Table(data, colWidths=[3.6*cm, 8.8*cm])
                table.setStyle(tablestyle_konklusion)

                kon_content.append(table)


                text_path = os.path.join(cache_main_dir,"Rapport","Tekst","Konklusion_above_5.md")

                if os.path.exists(text_path):
                    data = [["Målepunkt", "Tidspunkt for overskridelse"]]

                    kon_content.append(Spacer(0,12))

                    with open(text_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                    
                    kon_content.append(Paragraph(text, normal_text_style))

                    with open(os.path.join(cache_main_dir,"Rapport","Tekst","Konklusion_caption_above_5.md"), 'r', encoding='utf-8') as file:
                        text = file.read()


                    kon_cap_text = [[Paragraph(f"Tabel 3", caption_text_style), 
                            Paragraph(text, caption_text_style)]]
                    
                    kon_tab = Table(kon_cap_text, colWidths=[1.5*cm, 11.5*cm])
                    kon_tab.hAlign = 'LEFT'
                    kon_tab.setStyle(tablestyle_heading)
                    kon_content.append(kon_tab)


                    for adresse, details in trans_dict.items():
                        if details["above_limit_5"] == True:
                            result_path = os.path.join(cache_main_dir,"Rapport","Tekst",adresse)
                            text_bullet_path = os.path.join(result_path,"text_3.md")
                            bullet_points = []
                            if os.path.exists(text_bullet_path):
                                with open(text_bullet_path, 'r', encoding='utf-8') as file:
                                    for line in file:
                                        line = line.strip()
                                        if line.startswith("- "):
                                            text = line.split("Maksimal")[0]
                                            bullet_points.append(text[2:])
                            
                                bullet_text = "<br />".join(bullet_points)
                                data.append([Paragraph(f"{adresse}",table_text_style), Paragraph(bullet_text, table_text_style)])
                    
                    table = Table(data, colWidths=[3.6*cm, 8.8*cm])
                    table.setStyle(tablestyle_konklusion)

                    kon_content.append(table)


                kon_content.append(Spacer(0,12))
                
                if os.path.exists(os.path.join(cache_main_dir, "Rapport","Tekst","Konklusion_2.md")):
                    with open(os.path.join(cache_main_dir, "Rapport","Tekst","Konklusion_2.md"), 'r', encoding='utf-8') as file:
                        text = file.read()

                    kon_content.append(Paragraph(text, normal_text_style))
                    kon_content.append(Spacer(0,6))
                
            
            if os.path.exists(os.path.join(cache_main_dir, "Rapport","Tekst","Konklusion_3.md")):
                with open(os.path.join(cache_main_dir, "Rapport","Tekst","Konklusion_3.md"), 'r', encoding='utf-8') as file:
                    text = file.read()

                kon_content.append(Paragraph(text, normal_text_style))

            ### Bilag ###

            bilag_content = []
        
            for i, (adresse, details) in enumerate(trans_dict.items()):
                letter = danish_alphabet[i]

                bilag_title = Paragraph(f"Bilag {letter}{whitespace}{adresse}", heading7_style)
                bilag_content.append(bilag_title)

                if i != len(trans_dict) - 1:
                    bilag_content.append(PageBreak())


    
            ### Building PDF ###
            elements = []
            elements.extend(toc_content)
            elements.append(toc)
            elements.extend(bilag_toc_content)
            elements.append(PageBreak())
            elements.extend(ind_content)
            elements.extend(arb_content)
            elements.append(PageBreak())
            elements.extend(mål_content)
            elements.append(PageBreak())
            elements.extend(målKon_content)
            elements.extend(GrVr_content)
            elements.append(PageBreak())
            elements.extend(målRes_content)
            elements.append(PageBreak())
            elements.extend(kon_content)
            elements.append(PageBreak())
            elements.extend(bilag_content)


            pdf.multiBuild(elements)           
            #for i, section in enumerate(sections):
            #    page_number = page_tracker.section_page_numbers.get(section[1], "Unknown")
            #    toc_content[2*i+2] = Table([[Paragraph(section[0], toc_style), Paragraph(section[1], toc_style), Paragraph(str(page_number), toc_style)]], colWidths=[1 * cm, 10 * cm, 2 * cm], hAlign='LEFT') 
                    
            # Ensure the destination directory exists
            if os.name == 'nt':
                out_file_pdf = f'\\\\?\\{os.path.abspath(out_file_pdf)}'
            
            os.makedirs(os.path.dirname(out_file_pdf), exist_ok=True)
                
            if os.path.exists(out_file_pdf):
                os.remove(out_file_pdf)
            
            # Use os.rename to move the temporary PDF to the final path and rename it
            shutil.copy(temp_file_path, out_file_pdf)
            os.remove(temp_file_path)
        return out_file_pdf

    def merge_pdfs(pdf_list, output_file_pdf):
        from PySide6.QtWidgets import QMessageBox
        from PyPDF2 import PdfReader, PdfWriter

        pdf_writer = PdfWriter()
        for pdf_path in pdf_list:
            pdf_reader = PdfReader(pdf_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
                


        try:
            with open(output_file_pdf, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
        except PermissionError:
            logger.log(f"{output_file_pdf} er allerede åben. Luk filen og prøv igen.")
            reply = QMessageBox.critical(None, "Fejl", f"{output_file_pdf} er allerede åben. Luk filen og tryk herefter 'OK'.")
            while reply == QMessageBox.Ok:
                try:
                    with open(output_file_pdf, 'wb') as output_pdf:
                        pdf_writer.write(output_pdf)
                        break
                except PermissionError:
                    reply = QMessageBox.critical(None, "Fejl", f"{output_file_pdf} er allerede åben. Luk filen og tryk herefter 'OK'.")
                    
         
    def merge_appendix(cache_main_dir, main_file, info):
        from PyPDF2 import PdfReader, PdfWriter
        import re
        import time

        pattern = re.compile(r"_\d+$")  # Match "_n" folder pattern
        
        trans_dict = load_json(os.path.join(cache_main_dir,"Results","trans_dict_final.json"))

        main_pdf_reader = PdfReader(main_file)

        pdf_writer = PdfWriter()

        for page_num in range(len(main_pdf_reader.pages)):
            pdf_writer.add_page(main_pdf_reader.pages[page_num])
        
        n_appendix = len(trans_dict.keys())
        n_pages = len(main_pdf_reader.pages)

        insert_at_page = n_pages - n_appendix + 1

        def merge_pdf_from_folder(folder_path, adresse, pdf_writer, insert_at_page, subfolder = False):
            """Finds and adds PDFs in the correct order: 'Interval' first, 'Transients_list' second."""
            if not os.path.exists(folder_path):
                return
            
            if subfolder == True:
                insert_at_page -= 1

            # Get all PDFs
            pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

            # Sort: First 'Interval' PDFs, then 'Transients_list' PDFs
            interval_pdfs = sorted([os.path.join(folder_path, f) for f in pdf_files if "Interval" in f])
            transients_pdfs = sorted([os.path.join(folder_path, f) for f in pdf_files if "Transients_list" in f])

            n_pdf = len(interval_pdfs) + len(transients_pdfs)

            # Merge PDFs from the folder into the main PDF at the specified position
            for i, pdf in enumerate(interval_pdfs + transients_pdfs):                
                # Read the PDF
                try:
                    pdf_reader = PdfReader(pdf)
                except:
                    continue
                pdf_open = open(pdf, 'rb')
                n_pages = len(pdf_reader.pages)
                
                # Insert the pages at the specified position

                pdf_writer.merge(position=insert_at_page, fileobj = pdf_open, pages=(0, n_pages))

                if len(interval_pdfs) == 1:
                    if transients_pdfs != []:
                        if pdf == transients_pdfs[0]:
                            insert_at_page += n_pages + 1
                        else:
                            insert_at_page += n_pages
                    else:
                        insert_at_page += n_pages + 1
                else:
                    if i + 1 == n_pdf:
                        insert_at_page += n_pages + 1
                    else:
                        insert_at_page += n_pages
                    
                
                

            return insert_at_page


        for i, adresse in enumerate(trans_dict.keys()):
            logger.log(f"Tilføjer bilag fra {adresse}")
            folder_path = os.path.join(info["output_folder"], "INFRA", adresse.replace("/", " og "))

            # Step 1: Merge PDFs from the base folder
            insert_at_page = merge_pdf_from_folder(folder_path, adresse, pdf_writer, insert_at_page)

            # Step 2: Merge PDFs from _n subfolders in numerical order
            try:
                subfolders = sorted(
                    [d for d in os.listdir(folder_path) if pattern.match(d)],
                    key=lambda x: int(x[1:])  # Extract number and sort numerically
                )
            except FileNotFoundError:
                continue

            for subfolder in subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                insert_at_page = merge_pdf_from_folder(subfolder_path, adresse, pdf_writer, insert_at_page, subfolder=True)
        
        try:
            with open(main_file, 'wb') as file:
                pdf_writer.write(file)
        except PermissionError:
            time.sleep(5)
            try:
                with open(main_file, 'wb') as file:
                    pdf_writer.write(file)
            except PermissionError:
                logger.log("Noget gik galt med sammensætningen af pdf. Prøv igen og hvis problemet fortsætter, kontakt MLHU")
                return None
        
            
        return main_file

    #output_dir = info["output_folder"]
    pdf_final = info["pdf_path"]

    first_frontpage_file_pdf = create_first_front_page(cache_main_dir, info)
    second_frontpage_file_pdf = create_second_front_page(cache_main_dir, info)
    
    main_file_pdf = create_main_document(cache_main_dir, info)

    main_file_pdf = merge_appendix(cache_main_dir, main_file_pdf, info)
    if main_file_pdf == None:
        return

    pdf_list = [first_frontpage_file_pdf, second_frontpage_file_pdf, main_file_pdf]

    merge_pdfs(pdf_list, pdf_final)

    shutil.rmtree(os.path.join(cache_main_dir, "Temp"))

    os.startfile(pdf_final)



#info = load_json("JSON\\collected_data_hadsund.json")
#cache_main_dir = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-087 - Hadsundvej Syd, Gistrup"

#ReportGeneration(cache_main_dir, info)
