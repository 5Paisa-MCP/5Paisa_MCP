import creds
from py5paisa import FivePaisaClient
import json
import sys
import os

cred = {
    "APP_NAME": creds.app_name,
    "APP_SOURCE": creds.app_source,
    "USER_ID": creds.user_id,
    "PASSWORD": creds.password,
    "USER_KEY": creds.user_key,
    "ENCRYPTION_KEY": creds.encription_key
}

client = FivePaisaClient(cred=cred)

base_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(base_dir, "access_token.json")

with open(token_file, "r") as f:
    token_data = json.load(f)

client.set_access_token(token_data["access_token"], token_data["client_code"])

# Read CLI arguments
EID = int(sys.argv[1])

# Call API with only valid parameters
order = client.cancel_order(exch_order_id=EID)

print(json.dumps(order, indent=2))
