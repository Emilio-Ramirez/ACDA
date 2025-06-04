import pandas as pd
from unidecode import unidecode

xlsx_file = pd.ExcelFile("dataset.xlsx")
for sheet_name in xlsx_file.sheet_names:
    df = pd.read_excel("dataset.xlsx", sheet_name=sheet_name)
    dataset_name = unidecode(sheet_name).lower()
    df.to_parquet(f"datasets_raw/{dataset_name}.parquet")
    print(f"Guardado: {dataset_name}")
