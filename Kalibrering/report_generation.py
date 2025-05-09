def create_pdf(sensor_data, pdf_output, years, logo_img):
    from tkinter import messagebox
    from datetime import datetime
    import os
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.platypus import BaseDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, PageTemplate
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    import tempfile
    
    ## Input ##
    logo_width = 4 * cm  # Width of the logo
    logo_height = 1.5 * cm  # Height of the logo

    page_width, page_height = A4  # Get the dimensions of A4 paper

    styles = getSampleStyleSheet()

    bold_text = styles["Normal"].clone('bold_text_style')
    bold_text.fontName = "Times-Bold"
    bold_text.fontSize = 12
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        
        def add_logo(canvas, doc):
            if doc.page == 1:
                # Save the state of the canvas
                canvas.saveState()

                # Calculate X and Y position for the logo
                x_position = page_width - pdf.rightMargin - logo_width  # Align to the right margin
                y_position = page_height - pdf.topMargin - logo_height  # Align to the top margin

                # Draw the logo
                canvas.drawImage(logo_img, x_position, y_position, width=logo_width, height=logo_height, mask='auto')

                # Restore the state of the canvas
                canvas.restoreState()

        temp_file_path = os.path.join(tmpdirname, "temp_file.pdf")
        pdf = BaseDocTemplate(temp_file_path, pagesize=A4)

        # Define a Frame for the PageTemplate
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 2 * cm, id='normal')

        # Add the PageTemplate to the document
        pdf.addPageTemplates([PageTemplate(id='header_template', frames=frame, onPage=add_logo)])

        # Prepare table data
        table_data = [
            ['Type', 'ID', 'Sidste Kalibreringsdato', 'Kalibreringsstatus', 'Status', 'Sidste data hentet d.', 'Ejer']
        ]

        elements = []
        elements.append(Paragraph(f"Dato: {datetime.today().strftime('%Y-%m-%d')}. Kalibreringsstatus er baseret på en periode på {years} år.", bold_text))
        elements.append(Spacer(0,6))

        
        sorted_data = sorted(
            sensor_data.items(),
            key=lambda x: (
                x[1]["Ejer"],
                x[1]["Type"],
                datetime.strptime(x[1]["Kalibreringsdato"], "%Y-%m-%d") 
                if x[1]["Kalibreringsdato"] != "ukendt" else datetime.min  # Set "unknown" to a default date
            )
        )

        # Add data rows from the combined_data dictionary
        for key, data in sorted_data:
            row = [
                data["Type"],
                key,
                data['Kalibreringsdato'],  # Kalibreringsdato
                data['Kalibreringsstatus'],  # Kalibreringsstatus
                data['Status'],  # Status
                data['Sidste data hentet'],
                data['Ejer']  # Ejer
            ]
            table_data.append(row)

        # Create the table
        table = Table(table_data)

        # Set style for the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),  # Bold header
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data rows background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines
        ])

        # Apply the style
        table.setStyle(style)


        c = canvas.Canvas(temp_file_path, pagesize=A4)

        # Add the image to the top-right corner (adjust the coordinates as needed)

        # Coordinates for the top-right corner (adjust accordingly)
        c.drawImage(logo_img, page_width - 0.99 * cm - logo_width, page_height - 2.5 * cm, width=logo_width, height=logo_height, mask='auto')

        # Build the document with the table
        elements.append(table)
        pdf.build(elements)
        
        # Ensure the destination directory exists
        if os.name == 'nt':
            pdf_output = f'\\\\?\\{os.path.abspath(pdf_output)}'
        
        os.makedirs(os.path.dirname(pdf_output), exist_ok=True)
        
        # Use os.rename to move the temporary PDF to the final path and rename it
        try:
            if os.path.exists(pdf_output):
                os.remove(pdf_output)

            os.rename(temp_file_path, pdf_output)
        except PermissionError:
            messagebox.showerror("Fejl", f"{pdf_output} er allerede åben. Luk filen og prøv igen.")
            raise PermissionError("Filen kan ikke laves, da den allerede er åben. Luk filen og prøv igen.")
      