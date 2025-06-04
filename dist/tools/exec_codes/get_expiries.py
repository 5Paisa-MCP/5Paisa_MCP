import creds
from py5paisa import FivePaisaClient
import json
import sys
import os
import csv
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

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

EX = sys.argv[1]  
ASSET = sys.argv[2]


data = client.get_expiry(EX, ASSET)

print(data)  


