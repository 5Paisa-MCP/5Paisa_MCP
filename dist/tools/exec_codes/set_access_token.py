import creds
from py5paisa import FivePaisaClient
import json
import pyotp
import os
import requests
import pandas as pd
import io

def fetch_scrip_master(saving_path):
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/all"
    response = requests.get(url)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(io.StringIO(csv_data))  
        df.to_csv(saving_path, index=False)
        return df
    
    return None

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

    totp = pyotp.TOTP(creds.TOTP_SECRET).now()
    client.get_totp_session(creds.client_code,totp,creds.pin)

    access_token = client.get_access_token()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_file = os.path.join(base_dir, "access_token.json")

    with open(token_file, "w") as f:
        json.dump({
            "access_token": access_token,
            "client_code": creds.client_code
        }, f)

    print(access_token)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    saving_path = os.path.join(base_dir, "scrip_master.csv")
    scrip_df = fetch_scrip_master(saving_path)

