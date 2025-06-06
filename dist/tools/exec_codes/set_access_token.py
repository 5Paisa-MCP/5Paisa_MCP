import creds
from py5paisa import FivePaisaClient
import json

import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs

request_token_value = None

vendor_key = creds.user_key
PORT = 8000
response_url = f"http://127.0.0.1:{PORT}"
login_url = f"https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey={vendor_key}&ResponseURL={response_url}"


class TokenHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global request_token_value
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        request_token = query_params.get("RequestToken", [None])[0]

        if request_token:
            request_token_value = request_token
            print("\n Request token received:")
        else:
            print("No request_token found in the redirected URL.")

        # Respond to browser
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Login successful. You may now close this window.</h1>")

# === Function to launch login and get token ===
def get_request_token():
    global request_token_value
    webbrowser.open(login_url)

    with socketserver.TCPServer(("", PORT), TokenHandler) as httpd:
        httpd.handle_request()

    return request_token_value

if __name__ == "__main__":

    cred={
        "APP_NAME":creds.app_name,
        "APP_SOURCE":creds.app_source,
        "USER_ID":creds.user_id,
        "PASSWORD":creds.password,
        "USER_KEY":creds.user_key,
        "ENCRYPTION_KEY":creds.encription_key
        }

    client = FivePaisaClient(cred=cred)

    RequestToken = get_request_token()
    client.get_oauth_session(RequestToken)
    access_token = client.get_access_token()

    with open("access_token.json", "w") as f:
        json.dump({
            "access_token": access_token,
            "client_code": creds.client_code
        }, f)


