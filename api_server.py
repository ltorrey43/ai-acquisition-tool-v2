from flask import Flask, request, jsonify
import requests
import os

print("HARMONIC_API_KEY from env:", os.environ.get("HARMONIC_API_KEY"))

app = Flask(__name__)

# Load API Key from Render environment
HARMONIC_API_KEY = os.environ.get("HARMONIC_API_KEY")

@app.route("/query", methods=["POST"])
def query_companies():
    data = request.get_json()

    # Build query parameters for Harmonic API
    params = {}

    if data.get("company_name"):
        params["website_domain"] = data["company_name"]

    if data.get("location"):
        params["hq_locations"] = data["location"]

    params["size"] = 5  # Adjust as desired

    harmonic_url = "https://api.harmonic.ai/companies"

    headers = {
        "accept": "application/json",
        "apikey": HARMONIC_API_KEY
    }

    # Send POST request
    response = requests.post(harmonic_url, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({"error": f"Harmonic API error: {response.text}"}), 500

    harmonic_data = response.json()

    companies = harmonic_data.get("data", [])

    transformed = []
    for c in companies:
        transformed.append({
            "Company Name": c.get("legal_name"),
            "Description": c.get("description"),
            "Location": {
                "City": c.get("city"),
                "State": c.get("state"),
                "Country": c.get("country")
            },
            "Website": c.get("website"),
            "LinkedIn": c.get("linkedin"),
            "Headcount": c.get("headcount"),
            "Funding Total (USD M)": c.get("funding_total_usd_millions"),
            "Stage": c.get("stage"),
            "Last Funding Type": c.get("last_funding_type"),
            "Last Funding Date": c.get("last_funding_date"),
            "Last Funding Round Total (USD M)": c.get("last_funding_round_total_usd_millions"),
            "Last Valuation (USD M)": c.get("last_valuation_usd_millions"),
            "Investors": c.get("investors"),
            "Customer Type": c.get("customer_type"),
            "Market Vertical Tags": c.get("market_vertical_tags"),
            "Market Sub-Vertical Tags": c.get("market_sub_vertical_tags"),
            "Technology Tags": c.get("technology_tags"),
            "Company Highlights": c.get("company_highlights"),
            "Founders & CEOs": c.get("founders_and_ceos"),
            "Leadership's Prior Experiences": c.get("leadership_prior_experiences"),
            "Primary Contact Name": c.get("primary_contact_name"),
            "Primary Contact Email": c.get("primary_contact_email"),
            "Company Emails": c.get("company_emails"),
            "Team Emails": c.get("team_emails"),
            "Relevance Score": c.get("relevance_score"),
        })

    return jsonify(transformed)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)