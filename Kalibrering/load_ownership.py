def load_ownership_data(file_path):
    import pandas as pd
    df = pd.read_excel(file_path, sheet_name="Sheet1")  # Change "Sheet1" if necessary
    ownership_dict = df.set_index("ID")["Ejer"].to_dict()  # Assuming Excel columns are "ID" and "Owner"
    return ownership_dict