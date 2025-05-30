# Used to calculate the timeperiod

def calculate_date_from(date_submitted, output_dir):
    from datetime import timedelta
    import os

    date_to = date_submitted - timedelta(days=1)
    date_to = date_to.replace(hour=23, minute=59, second=0)

    if date_submitted.weekday() == 0:  # Monday
        date_from = date_to - timedelta(days=2)
    else:
        date_from = date_to
    
    date_from = date_from.replace(hour=0, minute=0, second=0)

    
    # Output filnavn
    if date_submitted.weekday() == 0:  # Mandag
        out_file_pdf = os.path.join(output_dir, f"Dagsrapport_{date_from.year}.{date_from.month}.{date_from.day}_{date_to.year}.{date_to.month}.{date_to.day}.pdf")
        date_range = f"{date_from.year}.{date_from.month}.{date_from.day} - {date_to.year}.{date_to.month}.{date_to.day}"
    else:
        out_file_pdf = os.path.join(output_dir, f"Dagsrapport_{date_to.year}.{date_to.month}.{date_to.day}.pdf")
        date_range = f"{date_to.year}.{date_to.month}.{date_to.day}"

    return date_to, date_from, date_range, out_file_pdf