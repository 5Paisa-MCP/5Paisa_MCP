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
QTY = int(sys.argv[2])
PR = float(sys.argv[3])
SLPR = float(sys.argv[4])

print(EID, QTY, PR, SLPR)

# Build parameters dictionary
order_params = {"ExchOrderID": EID}

if QTY != -1:
    order_params["Qty"] = QTY
if PR != float(-1):
    order_params["Price"] = PR
if SLPR != float(-1):
    order_params["StopLossPrice"] = SLPR

# Call API with only valid parameters
order = client.modify_order(**order_params)

print(json.dumps(order, indent=2))
