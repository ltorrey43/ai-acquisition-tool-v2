from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# ✅ Correct file path for cloud deployment
file_path = "valliance_pipeline.xlsx"

# Sheets to read
sheets = ["M&A", "M&A SL"]

# Load both sheets into a dictionary of DataFrames
dfs = pd.read_excel(file_path, sheet_name=sheets, engine="openpyxl")

# Clean up column names
for sheet_name, df in dfs.items():
    df.columns = df.columns.str.strip()

# Define search function
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

@app.route("/query", methods=["POST"])
def query_companies():
    # Parse JSON payload
    data = request.get_json()

    # Default to M&A SL sheet for searches
    df_ma_sl = dfs["M&A SL"]

    results = search_companies(
        df_ma_sl,
        company_name=data.get("company_name"),
        location=data.get("location"),
        employees_min=data.get("employees_min"),
        employees_max=data.get("employees_max"),
        revenue_min=data.get("revenue_min"),
        revenue_max=data.get("revenue_max"),
        keyword=data.get("keyword"),
    )

    if results.empty:
        return jsonify([])

    # Prepare clean JSON output
    output = results[[
        "Company Name",
        "Employees",
        "Location",
        "Revenue (USD M)",
        "Notes"
    ]].to_dict(orient="records")

    return jsonify(output)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)