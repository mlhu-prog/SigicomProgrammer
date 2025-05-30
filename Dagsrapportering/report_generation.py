

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from logger import get_logger

def create_footnotes(sensor_dict, df, cache_main_dir, cache_date, active = True, trans_dict = None, info_dict = None):
    from basic_functions import search_json, month_number_to_name, remove_suffix
    import pandas as pd

    foot_nr = 1

    footnote_dict = {}

    def format_date_time(date_time):
        return date_time.year, month_number_to_name(date_time.month), date_time.day, date_time.hour, date_time.minute

    def add_footnote(adresse, text):
        nonlocal foot_nr
        footnote_dict[adresse] = {"Footnote_Alarm": foot_note_alarm, "Foot_nr": f"{foot_nr}", "text": text}
        foot_nr += 1

    if active:
        for adresse in df["Adresse"]:
            df_temp = df[df["Adresse"] == adresse]

            text_adresse = remove_suffix(adresse)

            max_vib_percent = df_temp["Maks vib. [%]"].values[0]

            valid_comparison = False

            if isinstance(max_vib_percent, (int, float)):
                valid_comparison = max_vib_percent < 100
            elif isinstance(max_vib_percent, str):
                # Check if the string is a digit or can be converted to a float
                try:
                    num_value = float(max_vib_percent)
                    valid_comparison = num_value < 100
                except ValueError:
                    # If conversion fails, it's not a valid number
                    valid_comparison = False


            limit = df_temp["Grænse værdi"].values[0]
            
            cache_path = os.path.join(cache_main_dir, f'{adresse}')

            dat_file = os.path.join(cache_path,cache_date,"Ascii",f"data_flagged.dat")

            df_flag = pd.read_csv(dat_file, index_col=0, sep="\t")["Flag"].values
            
            transienter = trans_dict[adresse]

            if transienter != {}:
                n_slag = len(transienter["Transienter"])
            else:
                n_slag = 0
            
            if df_temp["Maks vib. [mm/s]"].values[0] == "-":
                footnote_dict[adresse] = {"Footnote_Alarm": 0, "Foot_nr":f"{0}"}

            elif float(df_temp["Maks vib. [mm/s]"].values[0]) > limit and trans_dict[adresse] != {} and 1 in df_flag and valid_comparison:
                info_dict[adresse]["fodnote_nr"] = foot_nr
                foot_note_alarm = 3
                    
                max_vib_mms = df_temp["Maks vib. [mm/s]"].values[0]
                max_vib_per = df_temp["Maks vib. [%]"].values[0]
                max_vib_fre = df_temp["Tilsvarende frekvens"].values[0]

                time_inc = pd.to_datetime(df_temp["Tidspunkt max vib."].values[0])
                year, month, day = format_date_time(time_inc)[:3]

                if n_slag == 1:
                    
                    date_trans = pd.to_datetime(transienter["Transienter"][0]["datetime"])

                    year_trans, month_trans, day_trans, hour_trans, minute_trans = format_date_time(date_trans)

                    text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                            f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                            f"for vibrationsfølsomme bygningskonstruktioner. Der er d. {day_trans}. {month_trans} {year_trans} kl. {hour_trans:02d}:{minute_trans:02d} " +
                            "registreret et slag på eller omkring sensoren." 
                    )
                    add_footnote(adresse, text)
                else:
                    
                    date_trans_start = pd.to_datetime(transienter["Transienter"][0]["datetime"])
                    date_trans_end = pd.to_datetime(transienter["Transienter"][-1]["datetime"])

                    year_trans_start, month_trans_start, day_trans_start, hour_trans_start, minute_trans_start = format_date_time(date_trans_start)
                    year_trans_end, month_trans_end, day_trans_end, hour_trans_end, minute_trans_end = format_date_time(date_trans_end)

                    if day_trans_start == day_trans_end:
                        if hour_trans_start != hour_trans_end or minute_trans_start != minute_trans_end:

                            text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                                    f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                                    f"for vibrationsfølsomme bygningskonstruktioner. Der er d. {day_trans_start}. {month_trans_start} {year_trans_start} fra " + 
                                    f"kl. {hour_trans_start:02d}:{minute_trans_start:02d} til kl. {hour_trans_end:02d}:{minute_trans_end:02d} registreret {int(n_slag)} slag på eller omkring sensoren." 
                            )
                            add_footnote(adresse, text)
                        else:

                            text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                                    f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                                    f"for vibrationsfølsomme bygningskonstruktioner. Der er d. {day_trans_start}. {month_trans_start} {year_trans_start} kl. " + 
                                    f"{hour_trans_start:02d}:{minute_trans_start:02d} registreret {int(n_slag)} slag på eller omkring sensoren." 
                            )
                            add_footnote(adresse, text)
                    else:

                        text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                                f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                                f"for vibrationsfølsomme bygningskonstruktioner. Der er fra {day_trans_start}. {month_trans_start} {year_trans_start} kl. " + 
                                f"{hour_trans_start:02d}:{minute_trans_start:02d} til kl. {day_trans_start}. {month_trans_start} {year_trans_start} kl. " + 
                                f"{hour_trans_end:02d}:{minute_trans_end:02d} registreret {int(n_slag)} slag på eller omkring sensoren." 
                        )
                        add_footnote(adresse, text)
            elif float(df_temp["Maks vib. [mm/s]"].values[0]) > limit and not 1 in df_flag and valid_comparison:
                
                foot_note_alarm = 2 # 

                max_vib_mms = df_temp["Maks vib. [mm/s]"].values[0]
                max_vib_per = df_temp["Maks vib. [%]"].values[0]
                max_vib_fre = df_temp["Tilsvarende frekvens"].values[0]

                time_inc = pd.to_datetime(df_temp["Tidspunkt max vib."].values[0])
                year, month, day = [time_inc.year, month_number_to_name(time_inc.month), time_inc.day]
                
                text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                        f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                        "for vibrationsfølsomme bygningskonstruktioner." 
                )
                
                add_footnote(adresse, text)

            elif trans_dict[adresse] != {} and 1 in df_flag:

                transienter = trans_dict[adresse]

                foot_note_alarm = 1

                if n_slag == 1:
                    
                    date_trans = pd.to_datetime(transienter["Transienter"][0]["datetime"])

                    year_trans, month_trans, day_trans, hour_trans, minute_trans = format_date_time(date_trans)

                    text = (f"{text_adresse}. Der er d. {day_trans}. {month_trans} {year_trans} kl. {hour_trans:02d}:{minute_trans:02d} " +
                            "registreret et slag på eller omkring sensoren." 
                    )
                    add_footnote(adresse, text)

                else:
                    
                    date_trans_start = pd.to_datetime(transienter["Transienter"][0]["datetime"])
                    date_trans_end = pd.to_datetime(transienter["Transienter"][-1]["datetime"])

                    year_trans_start, month_trans_start, day_trans_start, hour_trans_start, minute_trans_start = format_date_time(date_trans_start)
                    year_trans_end, month_trans_end, day_trans_end, hour_trans_end, minute_trans_end = format_date_time(date_trans_end)

                    if day_trans_start == day_trans_end:
                        if hour_trans_start != hour_trans_end or minute_trans_start != minute_trans_end:
                            text = (f"{text_adresse}. Der er d. {day_trans_start}. {month_trans_start} {year_trans_start} fra kl. {hour_trans_start:02d}:{minute_trans_start:02d} " +
                                    f"til kl. {hour_trans_end:02d}:{minute_trans_end:02d} registreret {int(n_slag)} slag på eller omkring sensoren." 
                            )
                            add_footnote(adresse, text)
                        elif hour_trans_start == hour_trans_end and minute_trans_start == minute_trans_end:
                            text = (f"{text_adresse}. Der er d. {day_trans_start}. {month_trans_start} {year_trans_start} kl. {hour_trans_start:02d}:{minute_trans_start:02d} " +
                                    f"registreret {int(n_slag)} slag på eller omkring sensoren." 
                            )
                            add_footnote(adresse, text)
                    else:
                        text = (f"{text_adresse}. Der er fra {day_trans_start}. {month_trans_start} {year_trans_start} kl. {hour_trans_start:02d}:{minute_trans_start:02d} " +
                                f"til kl. {day_trans_end}. {month_trans_end} {year_trans_end} kl. {hour_trans_end:02d}:{minute_trans_end:02d} registreret {int(n_slag)} slag på eller omkring sensoren." 
                        )
                        add_footnote(adresse, text)

            else:
                footnote_dict[adresse] = {"Footnote_Alarm": 0, "Foot_nr":f"{0}"}

        foot_note_list = search_json(footnote_dict, "Foot_nr")

        df.index = foot_note_list

        formatted_address = format_adress_by_footnote(df)
        df["Adresse"] = formatted_address

        footnote_notes = []

        # Iterate over footnote_dict
        for adresse, values in footnote_dict.items():
            foot_nr = values.get('Foot_nr', '0')
            text = values.get('text', '')
            
            # Check if Foot_nr is not equal to '0'
            if foot_nr != '0':
                # Construct the note format
                note = f"<super>{foot_nr})</super>{text}"
                footnote_notes.append(note)

        # Create DataFrame from the list of notes
        footnotes_df = pd.DataFrame({"note": footnote_notes})

        return footnotes_df
    else:
        for adresse in df["Adresse"]:
            df_temp = df[df["Adresse"] == adresse]

            text_adresse = remove_suffix(adresse)
    
            limit = df_temp["Grænse værdi"].values[0]
            
            try:
                max_vib_per_bool = float(df_temp["Maks vib. [%]"].values[0]) < int(100)
            except ValueError:
                max_vib_per_bool = True

            if isinstance(df_temp["Maks vib. [mm/s]"].values[0], str):
                footnote_dict[adresse] = {"Footnote_Alarm": 0, "Foot_nr":f"{0}"}
            elif float(df_temp["Maks vib. [mm/s]"].values[0]) > limit and max_vib_per_bool:
                
                foot_note_alarm = 2 # 

                max_vib_mms = df_temp["Maks vib. [mm/s]"].values[0]
                max_vib_per = df_temp["Maks vib. [%]"].values[0]
                max_vib_fre = df_temp["Tilsvarende frekvens"].values[0]

                time_inc = pd.to_datetime(df_temp["Tidspunkt max vib."].values[0])
                year, month, day = [time_inc.year, month_number_to_name(time_inc.month), time_inc.day]
                
                text = (f"{text_adresse}. Enkeltstående hændelse målt d. {day}. {month} {year} med et maksimalt vibrationsniveau på " +  
                        f"{max_vib_mms} mm/s ved {max_vib_fre} Hz svarende til ca. {max_vib_per} % af grænseværdien for bygningsskadelige vibrationer " + 
                        "for vibrationsfølsomme bygningskonstruktioner." 
                )
                
                add_footnote(adresse, text)
            else:
                footnote_dict[adresse] = {"Footnote_Alarm": 0, "Foot_nr":f"{0}"}


        foot_note_list = search_json(footnote_dict, "Foot_nr")

        df.index = foot_note_list

        formatted_address = format_adress_by_footnote(df)
        df["Adresse"] = formatted_address

        footnote_notes = []

        # Iterate over footnote_dict
        for adresse, values in footnote_dict.items():
            foot_nr = values.get('Foot_nr', '0')
            text = values.get('text', '')
            
            # Check if Foot_nr is not equal to '0'
            if foot_nr != '0':
                # Construct the note format
                note = f"<super>{foot_nr})</super>{text}"
                footnote_notes.append(note)

        # Create DataFrame from the list of notes
        footnotes_df = pd.DataFrame({"note": footnote_notes})

        return footnotes_df

def build_pdf(df, footnotes_df, atr, project, date_from, date_to, out_file_pdf):
    import tempfile
    from basic_functions import month_number_to_name, remove_suffix
    from PySide6.QtWidgets import QMessageBox

    logger = get_logger()
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = os.path.join(tmpdirname, 'temp_file.pdf')
        
        # Define the logo path and properties
        drive = "O:"
        rest_of_path = os.path.join("A000000", "A004371", "3_Pdoc", "Dagsrapportering", "files", "Logo.jpg")
        logo_path = os.path.normpath(drive + os.sep + rest_of_path)
        logo_width = 4 * cm  # Width of the logo
        logo_height = 1.5 * cm  # Height of the logo
        page_width, page_height = A4  # Page dimensions

        def add_header(canvas, doc):
            # Save the state of the canvas
            canvas.saveState()

            # First line (Bold, FontSize 12)
            header_line1 = project
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(1.77 * cm, 27.5 * cm, header_line1)

            # Second line (Normal, FontSize 10)
            header_line2 = atr
            canvas.setFont('Helvetica', 10)
            canvas.drawString(1.77 * cm, 26.9 * cm, header_line2)  # Adjust the Y position for the second line

            # Add page number at the bottom
            page_number_text = f"Side {doc.page}"
            canvas.setFont('Helvetica', 10)
            canvas.drawRightString(page_width - 2 * cm, 1 * cm, page_number_text)

            # Restore the state of the canvas
            canvas.restoreState()
        
        def add_logo(canvas, doc):
            if doc.page == 1:
                # Save the state of the canvas
                canvas.saveState()

                # Calculate X and Y position for the logo
                x_position = page_width - pdf.rightMargin - logo_width  # Align to the right margin
                y_position = page_height - pdf.topMargin - logo_height  # Align to the top margin

                # Draw the logo
                canvas.drawImage(logo_path, x_position, y_position, width=logo_width, height=logo_height)

                # Restore the state of the canvas
                canvas.restoreState()

        df['Adresse'] = df['Adresse'].apply(remove_suffix)

        # Extract headers and data
        data = df.values.tolist()

        # Add additional rows for the merged header structure
        # Default paragraph style for wrapped text
        styles = getSampleStyleSheet()

        # Define custom styles

        wrapped_style = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=8,
            alignment=1,  # Center alignment
            spaceAfter=6
        )

        wrapped_style_footnote = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=7,
            alignment=0,    # left alignment
            leftIndent= -1.08 * cm,  
            rightIndent= -1.08 * cm,  
            spaceAfter=6
        )

        wrapped_style_text_above_tabel = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=8,
            alignment=0,    # left alignment
            leftIndent= -1.08 * cm,  
            rightIndent= -1.08 * cm,  
            spaceAfter=0.3
        )

        wrapped_style_adresse = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=8,
            alignment=0,  # Left alignment
            spaceAfter=6
        )

        underlined_style = ParagraphStyle(
            name='Underlined',
            parent=styles['Normal'],
            fontSize=10,
            alignment=0,
            leftIndent= -1.08 * cm,  
            rightIndent= -1.08 * cm,  
            spaceAfter=0.3,
            us_lines=1  # Add underline
    )

        # Convert DataFrame rows to Paragraphs for wrapped text
        data = [
            [Paragraph(str(cell_value), wrapped_style_adresse if col_name in ["Adresse", "Postnummer"] else wrapped_style) 
            for col_name, cell_value in row.items()] 
            for index, row in df.iterrows()
        ]

        # Update the merged header structure with Paragraph for wrapped text
        merged_header_data = [
            [Paragraph("Adresse", wrapped_style_adresse), "", Paragraph("Grænseværdi", wrapped_style), 
            Paragraph("Sensor", wrapped_style), Paragraph("Serienr.", wrapped_style), Paragraph("Dato, opsat", wrapped_style), 
            Paragraph("Maks vibrationsniveau", wrapped_style), "", "", ""],
            ["", "", "", "", "", "", Paragraph("Hele måleperiode*", wrapped_style), "", Paragraph("Seneste døgn", wrapped_style), ""],
            ["", "", Paragraph("[mm/s]",wrapped_style), "", "", "", Paragraph("[mm/s]",wrapped_style), Paragraph("[%]",wrapped_style), Paragraph("[mm/s]",wrapped_style), Paragraph("[%]",wrapped_style)]
        ]

        # Your main text
        text_before_bold = "Det seneste døgn omfatter perioden:"
        
        day_to = date_to.day
        month_to = date_to.month
        day_from = date_from.day
        month_from = date_from.month
        
        if day_to == day_from and month_to == month_from:
            text_to_bold = f"{day_to}. {month_number_to_name(month_to)}"
        else:
            text_to_bold = f"{day_from}. {month_number_to_name(month_from)} - {day_to}. {month_number_to_name(month_to)}"

        # Combine the text, using HTML-like tags for bold
        combined_text = f"{text_before_bold} <b>{text_to_bold}</b>"

        underlined_text = Paragraph("Igangværende målinger:", underlined_style)

        # Create a PDF document with a custom PageTemplate
        pdf = BaseDocTemplate(temp_file_path, pagesize=A4)

        # Define a Frame for the PageTemplate
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')

        # Add the PageTemplate to the document
        pdf.addPageTemplates([PageTemplate(id='header_template', frames=frame, onPage=add_header, onPageEnd=add_logo)])

        table_header = Paragraph(combined_text, wrapped_style_text_above_tabel)

        # Create the merged table
        table = Table(merged_header_data + data, colWidths=[2.96 * cm, 2.65 * cm, 1.45 * cm, 1.32 * cm, 1.43 * cm, 1.96 * cm, 1.53 * cm, 1.43 * cm, 1.53 * cm, 1.32 * cm])

        # Add a TableStyle with grid and span instructions
        style = TableStyle([
            ('SPAN', (0, 0), (1, 2)),  # Merge cells for "Adresse"
            ('SPAN', (2, 0), (2, 1)),  # Merge cells for "Grænse værdi"
            ('SPAN', (3, 0), (3, 2)),  # Merge cells for "Logger,"
            ('SPAN', (4, 0), (4, 2)),  # Merge cells for "Sensor,"
            ('SPAN', (5, 0), (5, 2)),  # Merge cells for "Dato, opsat"
            ('SPAN', (6, 0), (9, 0)),  # Merge cells for "Maksimal vibrationsniveau,"
            ('SPAN', (6, 1), (7, 1)),  # Merge cells for "Hele måleperiode*"
            ('SPAN', (8, 1), (9, 1)),  # Merge cells for "Seneste døgn*"
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),  # Set background color for the first row
            ('BACKGROUND', (0, 1), (-1, 1), colors.darkorange),  # Set background color for the second row
            ('BACKGROUND', (0, 2), (-1, 2), colors.darkorange),  # Set background color for the third row
            ('TEXTCOLOR', (0, 0), (-1, 2), colors.whitesmoke),  # Set text color for the first and second rows
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Align all cells to "left"
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle align all cells
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),  # Bold font for the first and second rows
            ('GRID', (0, 3), (-1, -1), 0.5, colors.gray),  # Grid lines
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the entire table
        ])

        table.setStyle(style)

        # Text to add below the table
        footer_text = Paragraph(
            "* Vibrationsniveauet for C22 logger er angivet i reelle data samt frekvensvægtet med en procentværdi relativ til valgte grænseværdi. Vibrationsniveauet for øvrige loggere er frekvensvægtede værdier.",
            wrapped_style_footnote)

        # Generate footnotes from the footnotes DataFrame
        footnotes = [Paragraph(str(footnote), wrapped_style_footnote) for footnote in footnotes_df["note"]]

        # Build the PDF
        elements = [underlined_text, table_header, Spacer(1, 0.2 * cm), table, Spacer(1, 0.5 * cm)]
        elements.extend(footnotes)  # Add footnotes to the list of elements
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(footer_text)  # Add footer text to the list of elements

        pdf.build(elements)
        
        # Ensure the destination directory exists
        if os.name == 'nt':
            out_file_pdf = f'\\\\?\\{os.path.abspath(out_file_pdf)}'
        
        if os.path.exists(out_file_pdf):
            try:
                os.remove(out_file_pdf)
            except PermissionError:
                QMessageBox.critical(None, "Fejl", "{} er allerede åben. Luk filen og prøv igen.".format(os.path.basename(out_file_pdf)))
                logger.log("{} er allerede åben. Luk denne og 'Hent data og generer rapport' igen!".format(os.path.basename(out_file_pdf)),2,1)
        
        if not os.path.dirname(out_file_pdf):
            os.makedirs(os.path.dirname(out_file_pdf), exist_ok=True)
        
        # Use os.rename to move the temporary PDF to the final path and rename it
        try:
            os.rename(temp_file_path, out_file_pdf)
        except (PermissionError, FileExistsError) as e:
            if isinstance(e, FileExistsError):
                QMessageBox.warning(None, "Fejl", "Der skete en fejl ved at oprette pdf'en. Prøv igen.")
            else:
                QMessageBox.critical(None, "Fejl", f"{out_file_pdf} er allerede åben. Luk filen og prøv igen.")
                raise PermissionError("Filen kan ikke laves, da den allerede er åben. Luk filen og prøv igen.")
            

    return pdf.page

def build_pdf_ended_measurements(df, footnotes_df, end_page, out_file_pdf):
    import tempfile
    from basic_functions import remove_suffix

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = os.path.join(tmpdirname, 'temp_file.pdf')
    
        def add_header(canvas, doc, end_page):
            # Save the state of the canvas
            canvas.saveState()

            page_width, _ = A4  # Page dimension

            # Add page number at the bottom
            page_number_text = f"Side {doc.page + end_page}"
            canvas.setFont('Helvetica', 10)
            canvas.drawRightString(page_width - 2 * cm, 1 * cm, page_number_text)

            # Restore the state of the canvas
            canvas.restoreState()

        class CustomPageTemplate(PageTemplate):
            def __init__(self, id, frames, onPage, end_page):
                super().__init__(id=id, frames=frames, onPage=self.on_page_wrapper(onPage))
                self.end_page = end_page

            def on_page_wrapper(self, onPage):
                def wrapped(canvas, doc):
                    onPage(canvas, doc, self.end_page)
                return wrapped

        
        # Extract headers and data
        df['Adresse'] = df['Adresse'].apply(remove_suffix)

        data = df.values.tolist()

        # Add additional rows for the merged header structure
        # Default paragraph style for wrapped text
        styles = getSampleStyleSheet()

        # Define custom styles

        wrapped_style = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=8,
            alignment=1,  # Center alignment
            spaceAfter=6
        )

        wrapped_style_footnote = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=7,
            alignment=0,    # left alignment
            leftIndent= -0.68* cm,  
            rightIndent= -0.68 * cm,  
            spaceAfter=6
        )

        wrapped_style_adresse = ParagraphStyle(
            name='Wrapped',
            parent=styles['Normal'],
            fontSize=8,
            alignment=0,  # Left alignment
            spaceAfter=6
        )

        underlined_style = ParagraphStyle(
            name='Underlined',
            parent=styles['Normal'],
            fontSize=10,
            alignment=0,
            leftIndent= -0.68 * cm,  
            rightIndent= -0.68 * cm,  
            spaceAfter=0.3,
            us_lines=1  # Add underline
    )

        # Convert DataFrame rows to Paragraphs for wrapped text
        data = [
            [Paragraph(str(cell_value), wrapped_style_adresse if col_name in ["Adresse", "Postnummer"] else wrapped_style) 
            for col_name, cell_value in row.items()] 
            for index, row in df.iterrows()
        ]

        # Update the merged header structure with Paragraph for wrapped text
        merged_header_data = [
            [Paragraph("Adresse", wrapped_style_adresse), "", Paragraph("Grænseværdi", wrapped_style), 
            Paragraph("Sensor", wrapped_style), Paragraph("Serienr.", wrapped_style), Paragraph("Dato", wrapped_style), "", 
            Paragraph("Maks vibrationsniveau", wrapped_style), ""],
            ["", "", "", "", "", Paragraph("Opsat", wrapped_style), Paragraph("Nedtaget", wrapped_style), Paragraph("Hele måleperioden*", wrapped_style), ""],
            ["", "", Paragraph("[mm/s]",wrapped_style), "", "", "", "", Paragraph("[mm/s]",wrapped_style), Paragraph("[%]",wrapped_style)]
        ]

        underlined_text = Paragraph("Afsluttede målinger:", underlined_style)

        # Create a PDF document with a custom PageTemplate
        pdf = BaseDocTemplate(temp_file_path, pagesize=A4)

        # Define a Frame for the PageTemplate
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')

        # Add the PageTemplate to the document
        pdf.addPageTemplates([CustomPageTemplate(id='header_template', frames=frame, onPage=add_header, end_page=end_page)])



        # Create the merged table
        table = Table(merged_header_data + data, colWidths=[2.96 * cm, 2.65 * cm, 1.45 * cm, 1.32 * cm, 1.43 * cm, 1.96 * cm, 1.96 * cm, 1.53 * cm, 1.53 * cm])

        # Add a TableStyle with grid and span instructions
        style = TableStyle([
            ('SPAN', (0, 0), (1, 2)),  # Merge cells for "Adresse"
            ('SPAN', (2, 0), (2, 1)),  # Merge cells for "Grænse værdi"
            ('SPAN', (3, 0), (3, 2)),  # Merge cells for "Logger,"
            ('SPAN', (4, 0), (4, 2)),  # Merge cells for "Sensor,"
            ('SPAN', (5, 0), (6, 0)),  # Merge cells for "Dato"
            ('SPAN', (7, 0), (8, 0)),  # Merge cells for "Maksimal vibrationsniveau,"
            ('SPAN', (7, 1), (8, 1)),  # Merge cells for "Hele måleperiode*"
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),  # Set background color for the first row
            ('BACKGROUND', (0, 1), (-1, 1), colors.darkorange),  # Set background color for the second row
            ('BACKGROUND', (0, 2), (-1, 2), colors.darkorange),  # Set background color for the third row
            ('TEXTCOLOR', (0, 0), (-1, 2), colors.whitesmoke),  # Set text color for the first and second rows
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Align all cells to "left"
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle align all cells
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica-Bold'),  # Bold font for the first and second rows
            ('GRID', (0, 3), (-1, -1), 0.5, colors.gray),  # Grid lines
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the entire table
        ])

        table.setStyle(style)

        # Text to add below the table
        footer_text = Paragraph(
            "* Vibrationsniveauet for C22 logger er angivet i reelle data samt frekvensvægtet med en procentværdi relativ til valgte grænseværdi. Vibrationsniveauet for øvrige loggere er frekvensvægtede værdier.",
            wrapped_style_footnote)

        # Generate footnotes from the footnotes DataFrame
        footnotes = [Paragraph(str(footnote), wrapped_style_footnote) for footnote in footnotes_df["note"]]

        # Build the PDF
        elements = [underlined_text, Spacer(1, 0.2 * cm), table, Spacer(1, 0.5 * cm)]
        elements.extend(footnotes)  # Add footnotes to the list of elements
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(footer_text)  # Add footer text to the list of elements

        pdf.build(elements)
            
        # Ensure the destination directory exists
        if os.name == 'nt':
            out_file_pdf = f'\\\\?\\{os.path.abspath(out_file_pdf)}'
        
        os.makedirs(os.path.dirname(out_file_pdf), exist_ok=True)
            
        # Use os.rename to move the temporary PDF to the final path and rename it
        if os.path.exists(out_file_pdf):
            os.remove(out_file_pdf)
        
        # Use os.rename to move the temporary PDF to the final path and rename it
        os.rename(temp_file_path, out_file_pdf)

def merge_pdfs(pdf_list, output_file_pdf):
    from PyPDF2 import PdfReader, PdfWriter
    from PySide6.QtWidgets import QMessageBox
    
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
        QMessageBox.critical(None, "Fejl", f"{output_file_pdf} er allerede åben. Luk filen og prøv igen.")
        raise PermissionError("Filen kan ikke laves, da den er åben")


    for pdf_path in pdf_list: 
        os.remove(pdf_path)

    #print(f"{output_file_pdf} has been created")

def format_adress_by_footnote(df):
    # Track the count of non-zero indices
    formatted_addresses = []

    for index, row in df.iterrows():
        idx = int(index)
        address = row['Adresse']
        
        if idx == 0:
            formatted_addresses.append(address)
        else:
            formatted_address = f"{address}<super>{idx})</super>"
            formatted_addresses.append(formatted_address)

    return formatted_addresses

