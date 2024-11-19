import streamlit as st
import pandas as pd
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from fetch_data import fetch_search_results
from clean_data import clean_json_data
from extract_info_mo import extract_info
from agent import TaskManager
from dotenv import load_dotenv

load_dotenv()

# Define the scope for Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

task_manager = TaskManager()

def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    return service

def read_google_sheet(sheet_id, range_name="Sheet1"):
    service = authenticate_google()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    data = result.get('values', [])
    return pd.DataFrame(data[1:], columns=data[0])

def update_google_sheet(sheet_id, df, range_name="Sheet1"):
    service = authenticate_google()
    body = {
        "values": [df.columns.tolist()] + df.values.tolist()
    }
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

def main():
    st.title("Entity Info Extractor")

    option = st.radio("Select input source:", ("Upload CSV", "Link Google Sheet"))

    df = None
    sheet_id = None

    if option == "Upload CSV":
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

    elif option == "Link Google Sheet":
        sheet_id = st.text_input("Enter the Google Sheet ID:")
        if sheet_id:
            try:
                df = read_google_sheet(sheet_id)
                st.success("Google Sheet data loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load Google Sheet: {e}")

    if df is not None:
        st.write("### Uploaded Data", df.head())
        info_input = st.text_input("Enter info(s) you want to extract (separate by commas):", "")
        
        google_api_key = os.getenv('google_api_key')
        groq_api_key = os.getenv("groq_api_key")

        if st.button("Start Processing"):
            if not info_input or not google_api_key or not groq_api_key:
                st.error("Please provide the necessary inputs (Info(s), Google API Key, Groq API Key).")
            else:
                info_list = [info.strip() for info in info_input.split(",")]
                st.info("Processing... Please wait.")
                
                for info in info_list:
                    df[info] = None  # Initialize column for each info

                for index, row in df.iterrows():
                    entity = row['entity']
                    
                    for info in info_list:
                        try:
                            task_manager.execute_task(fetch_search_results, entity, info, google_api_key)
                            task_manager.execute_task(clean_json_data, "search_results.json", "cleaned_results.json")
                            extracted_data = task_manager.execute_task(extract_info, entity, info, groq_api_key)

                            trimmed_data = extracted_data.split(":", 1)[-1].strip()
                            df.at[index, info] = trimmed_data
                        except Exception as e:
                            st.error(f"Error processing entity '{entity}' with info '{info}': {e}")
                
                st.write("### Processed Data", df)

                if option == "Upload CSV":
                    csv_file = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Updated CSV",
                        data=csv_file,
                        file_name="updated_data.csv",
                        mime="text/csv"
                    )
                
                elif option == "Link Google Sheet":
                    try:
                        update_google_sheet(sheet_id, df)
                        st.success("Google Sheet updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating Google Sheet: {e}")

if __name__ == "__main__":
    main()
