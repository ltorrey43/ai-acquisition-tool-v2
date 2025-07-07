import pandas as pd

file_path = "/Users/luketorrey/Documents/ai-acquisition-tool v2/valliance_pipeline.xlsx"

sheets = ["M&A", "M&A SL"]
dfs = pd.read_excel(file_path, sheet_name=sheets, engine="openpyxl")

for sheet_name, df in dfs.items():
    df.columns = df.columns.str.strip()
    print(f"Sheet: {sheet_name}")
    print("Columns:", df.columns.tolist())
    print(df.head(), "\n")

def search_companies(
    df,
    company_name=None,
    location=None,
    employees_min=None,
    employees_max=None,
    revenue_min=None,
    revenue_max=None,
    keyword=None
):
    filtered = df.copy()

    if company_name:
        filtered = filtered[
            filtered["Company Name"].str.contains(company_name, case=False, na=False)
        ]

    if location:
        filtered = filtered[
            filtered["Location"].str.contains(location, case=False, na=False)
        ]

    if employees_min is not None:
        filtered = filtered[filtered["Employees"] >= employees_min]

    if employees_max is not None:
        filtered = filtered[filtered["Employees"] <= employees_max]

    if revenue_min is not None:
        filtered = filtered[filtered["Revenue (USD M)"] >= revenue_min]

    if revenue_max is not None:
        filtered = filtered[filtered["Revenue (USD M)"] <= revenue_max]

    if keyword:
        filtered = filtered[
            filtered["Notes"].str.contains(keyword, case=False, na=False)
        ]

    return filtered

# Single test guaranteed to return results
df_ma_sl = dfs["M&A SL"]
df_ma_sl.columns = df_ma_sl.columns.str.strip()

results = search_companies(
    df_ma_sl,
    keyword="Databricks"
)

if results.empty:
    print("No matching companies found.")
else:
    for _, row in results.iterrows():
        print(f"- {row['Company Name']}")
        print(f"  Location: {row['Location']}")
        print(f"  Employees: {row['Employees']}")
        print(f"  Revenue (USD M): {row['Revenue (USD M)']}")
        print(f"  Notes: {row['Notes']}")
        print()