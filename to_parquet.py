import pandas as pd

# Leer todas las hojas
xlsx_file = pd.ExcelFile("dataset.xlsx")
for sheet_name in xlsx_file.sheet_names:
    df = pd.read_excel("dataset.xlsx", sheet_name=sheet_name)
    df.to_parquet(f"datasets_raw/{sheet_name}.parquet")
