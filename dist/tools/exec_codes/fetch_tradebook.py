import creds
from py5paisa import FivePaisaClient
import json
import os

cred={
    "APP_NAME":creds.app_name,
    "APP_SOURCE":creds.app_source,
    "USER_ID":creds.user_id,
    "PASSWORD":creds.password,
    "USER_KEY":creds.user_key,
    "ENCRYPTION_KEY":creds.encription_key
    }


client = FivePaisaClient(cred=cred)

base_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(base_dir, "access_token.json")

with open(token_file, "r") as f:
    token_data = json.load(f)

client.set_access_token(token_data["access_token"], token_data["client_code"])

obook = client.get_tradebook()
print(json.dumps(obook))  # MUST be pure JSON output

