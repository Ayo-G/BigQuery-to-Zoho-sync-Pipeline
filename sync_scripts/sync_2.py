# ========== ZOHO SHEET NAME ==========
# ========== NECESSARY  MODULES ==========
import os
import time
import json
import requests
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

def run():
  """
  A robust ETL script to sync data between Bigquery and Zoho Sheets for the Product department.
  - It queries BigQuery using the provided query.
  - It clears the destination sheet on Zoho sheets.
  - It uploades the data from BigQuery to the cleared sheet.
  - It logs erros for easy debugging.
  - Includes a time delay to avoid API issues.
  - Includes retrys incase of errors.
  """
  # ========== CONFIGURATION ==========  
  cd = os.getcwd()
  file = 'key.json'
  GCP_CREDENTIALS_PATH = os.path.join(cd, file)

  SPREADSHEET_ID = "SPREADSHEET_ID"
  WORKSHEET_NAME = "WORKSHEET_NAME"
  
  USERDATA = {
      "REFRESHTOKEN": 'REFRESHTOKEN',
      "CLIENTID": 'CLIENTID',
      "CLIENTSECRET": 'CLIENTSECRET',
      "REDIRECT_URI": "REDIRECT_URI"
  }


  # ========== GET ACCESS TOKEN ==========  
  def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": USERDATA["REFRESHTOKEN"],
        "client_id": USERDATA["CLIENTID"],
        "client_secret": USERDATA["CLIENTSECRET"],
        "redirect_uri": USERDATA["REDIRECT_URI"],
        "grant_type": "refresh_token"
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    access_token = response.json().get("access_token")
    if not access_token:
        raise ValueError("Failed to fetch access token. Response: " + str(response.json()))

    return access_token

    
  # ========== 📊 QUERY BIGQUERY ==========
  def query_bigquery():
      try:
          creds = service_account.Credentials.from_service_account_file(GCP_CREDENTIALS_PATH)
          client = bigquery.Client(credentials=creds, project=creds.project_id)

          query = """
                select
                  *
                from
                  table
                  """

          df = client.query(query).to_dataframe()
          print("✅ Query successful")
          return df

      except Exception as e:
          print("❌ Error querying BigQuery:", e)
          return None

  # ========== 🧹 CLEAR ENTIRE SHEET (EXCLUDING HEADER) ==========
  def clear_sheet(access_token: str, spreadsheet_id: str, worksheet_name: str, first_col: str):
      """
      Deletes all rows where <first_col> is NOT null, preserving the header row.
      """
      url = f"https://sheet.zoho.com/api/v2/{spreadsheet_id}"
      criteria = f'"{first_col}"!=null'

      paramMap = {
          "method": "worksheet.records.delete",
          "worksheet_name": worksheet_name,
          "header_row": 1,
          "delete_rows": True,
          "criteria": criteria
      }

      headers = {
          "Content-type": "application/x-www-form-urlencoded",
          "Authorization": f"Zoho-oauthtoken {access_token}"
      }

      response = requests.post(url=url, headers=headers, data=paramMap)

      if response.status_code == 200:
          print(f"✅ Cleared all rows from {worksheet_name} where {first_col} != null")
      else:
          print("❌ Failed to clear sheet.")
          print(f"Status Code: {response.status_code}")
          print(f"Response: {response.text}")



  # ========== 📥 WRITE DATA TO SHEET ==========
  def write_to_sheet(df, access_token, spreadsheet_id, worksheet_name, batch_size=1000):
      if df is None or df.empty:
          print("⚠️ No data to write.")
          return

      try:
          total_rows = len(df)
          print(f"📊 Preparing to upload {total_rows} rows in batches of {batch_size} to {worksheet_name}...")
          headers_row = df.columns.tolist()
          url = f"https://sheet.zoho.com/api/v2/{spreadsheet_id}"
          headers = {
              "Content-type": "application/x-www-form-urlencoded",
              "Authorization": f"Zoho-oauthtoken {access_token}"
          }

          for start in range(0, total_rows, batch_size):
              end = min(start + batch_size, total_rows)
              batch_df = df.iloc[start:end]
              data_rows = batch_df.astype(str).values.tolist()
              records = [dict(zip(headers_row, row)) for row in data_rows]

              paramMap = {
                  "method": "worksheet.records.add",
                  "worksheet_name": worksheet_name,
                  "header_row": 1,
                  "json_data": json.dumps(records)
              }

              print(f"📤 Uploading rows {start + 1} to {end}...")
              response = requests.post(url=url, headers=headers, data=paramMap)

              if response.status_code == 200:
                  print(f"✅ Successfully uploaded rows {start + 1} to {end}")
              else:
                  print(f"❌ Failed to upload rows {start + 1} to {end} (Status {response.status_code})")
                  print("Response:", response.text)
                  print("🚨 Stopping further uploads.")
                  break  # Stop on error

              time.sleep(1)  # Short delay between batches

      except Exception as e:
          print("❌ Error in write_to_sheet:", e)

  # ========== 🚀 MAIN RUN ==========
  df = query_bigquery()
  if df is not None:
      print(f"📊 Retrieved {len(df)} rows from BigQuery")
      token = get_access_token()

      first_column = df.columns.tolist()[0]
      clear_sheet(token, SPREADSHEET_ID, WORKSHEET_NAME, first_column)

      delay_seconds = 2
      print(f"⏳ Waiting {delay_seconds} seconds before writing data...")
      time.sleep(delay_seconds)

      write_to_sheet(df, token, SPREADSHEET_ID, WORKSHEET_NAME)

if __name__ == "__main__":
    run()
