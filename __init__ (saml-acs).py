import azure.functions as func
import base64
import xml.etree.ElementTree as ET
import urllib.parse

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        saml_response = req.form.get("SAMLResponse")
        if not saml_response:
            return func.HttpResponse("Missing SAMLResponse", status_code=400)

        # Decode Base64-encoded SAML
        decoded_data = base64.b64decode(saml_response)
        root = ET.fromstring(decoded_data)

        ns = {
            "saml": "urn:oasis:names:tc:SAML:2.0:assertion"
        }

        # Extract username (from NameID or custom attribute)
        name_id = root.find(".//saml:Subject/saml:NameID", ns)
        username = name_id.text if name_id is not None else "UnknownUser"

        # Extract department from custom attribute
        department = "Unknown"
        for attr in root.findall(".//saml:Attribute", ns):
            if attr.attrib.get("Name") == "department":
                department = attr.find(".//saml:AttributeValue", ns).text
                break

        # Redirect to static app with user info
        redirect_url = f"https://simpleapp1.z27.web.core.windows.net/?username={urllib.parse.quote(username)}&department={urllib.parse.quote(department)}"
        return func.HttpResponse(
            status_code=302,
            headers={"Location": redirect_url}
        )

    except Exception as e:
        return func.HttpResponse(f"Error processing SAML: {str(e)}", status_code=500)
