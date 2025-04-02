import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle OPTIONS preflight request for CORS
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
    
    try:
        # Attempt to get the JSON payload from the request
        data = req.get_json()

        # Retrieve values for username, role, and department from the payload
        username = data.get("username")
        department = data.get("department")

        # Check for missing fields and return a 400 Bad Request if necessary
        if not username or not department:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: username, department"}),
                status_code=400,
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Simple Access Control Logic
        if department == "IT":
            # Access granted for IT Vendor
            return func.HttpResponse(
                json.dumps({"access": "granted", "username": username, "department": department}),
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        elif department == "Sales":
            # Sales users only get access to sales-related features
            return func.HttpResponse(
                json.dumps({"access": "restricted", "username": username, "department": department}),
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        elif department == "Marketing":
            # Marketing users get restricted access
            return func.HttpResponse(
                json.dumps({"access": "restricted", "username": username, "department": department}),
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        else:
            # Users from other departments may have no access
            return func.HttpResponse(
                json.dumps({"access": "denied", "username": username, "department": department}),
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"}
            )

    except Exception as e:
        # Return error response with the exception message
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            headers={"Access-Control-Allow-Origin": "*"}
        )
