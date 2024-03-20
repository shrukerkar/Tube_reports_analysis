import requests
from datetime import datetime

def get_tube_disruption_reports():
    """
    Fetches latest tube line disruption reports from the TfL API and returns a list of reports for the current date.
    """

    # Send API request
    url = 'https://api.tfl.gov.uk/Line/Mode/tube/Status'
    response = requests.get(url)

    # Handle response
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error fetching data: {response.status_code}")

    # Get current date
    current_date = datetime.utcnow().strftime("%Y-%m-%d")

    # Extract relevant data
    tube_reports = []
    for line in data:
        try:
            line_name = line["name"]
            status = line["lineStatuses"][0]["statusSeverityDescription"]
            disruption_datetime = line["lineStatuses"][0]["validityPeriods"][0]["fromDate"]
            disruption_date = datetime.strptime(disruption_datetime, "%Y-%m-%dT%H:%M:%SZ").date().strftime("%Y-%m-%d")
            disruption_reason = line["lineStatuses"][0]["reason"]  # Assuming reason is not always available

            if current_date == disruption_date:
                report = {
                    "current_timestamp": disruption_datetime,
                    "line": line_name,
                    "status": status,
                    "disruption_reason": disruption_reason
                }
                tube_reports.append(report)
        except Exception as e:
            disruption_reason = None
            distruption_date =None

    return tube_reports

# Get latest Report
# reports = get_tube_disruption_reports()
# print(reports)