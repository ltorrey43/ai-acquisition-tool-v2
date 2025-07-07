import pandas as pd
from flask import Flask, request, jsonify

# Load your Excel file
file_path = "/Users/luketorrey/Documents/ai-acquisition-tool v2/valliance_pipeline.xlsx"
sheets = ["M&A", "M&A SL"]
dfs = pd.read_excel(file_path, sheet_name=sheets, engine="openpyxl")

# Clean up column names for all sheets
for sheet_name, df in dfs.items():
    df.columns = df.columns.str.strip()

# Your filtering function
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

# Initialize Flask app
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    # Get JSON payload
    data = request.get_json()

    df_ma_sl = dfs["M&A SL"]
    df_ma_sl.columns = df_ma_sl.columns.str.strip()

    # Extract filters from the request
    filters = {
        "company_name": data.get("company_name"),
        "location": data.get("location"),
        "employees_min": data.get("employees_min"),
        "employees_max": data.get("employees_max"),
        "revenue_min": data.get("revenue_min"),
        "revenue_max": data.get("revenue_max"),
        "keyword": data.get("keyword")
    }

    # Run search
    results = search_companies(df_ma_sl, **filters)

    # Only return selected columns for clarity
    if not results.empty:
        results = results[
            ["Company Name", "Location", "Employees", "Revenue (USD M)", "Notes"]
        ]

    # Convert to JSON
    results_json = results.to_dict(orient="records")
    return jsonify(results_json)

if __name__ == "__main__":
    app.run(port=5000, debug=True)