import pandas as pd

# ✅ Use relative path for cloud deploy
file_path = "valliance_pipeline.xlsx"

# Sheets to read
sheets = ["M&A", "M&A SL"]

# Load both sheets into a dictionary of DataFrames
dfs = pd.read_excel(file_path, sheet_name=sheets, engine="openpyxl")

# Clean up column names
for sheet_name, df in dfs.items():
    df.columns = df.columns.str.strip()
    print(f"Sheet: {sheet_name}")
    print("Columns:", df.columns.tolist())
    print(df.head(), "\n")