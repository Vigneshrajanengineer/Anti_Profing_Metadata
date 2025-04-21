import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

st.set_page_config(page_title="Anti_profing_Metadata", layout="centered")
st.title("Anti_profing_MetaData-User Excel Sheet Merger")

DATA_FILE = "master_merged_data.xlsx"

# Load existing data
if os.path.exists(DATA_FILE):
    master_df = pd.read_excel(DATA_FILE)
else:
    master_df = pd.DataFrame()

uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx", "xls"], accept_multiple_files=True)
user_name = st.text_input("Enter your name or identifier:")
sheet_name = st.text_input("Sheet name to merge (optional)", value="")

if st.button("Merge Files"):
    if not uploaded_files or not user_name:
        st.warning("Please upload files and enter your name.")
    else:
        dfs = []
        for file in uploaded_files:
            try:
                df = pd.read_excel(file, sheet_name=sheet_name if sheet_name else 0)
                df["UploadedBy"] = user_name
                df["FileName"] = file.name
                df["UploadTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dfs.append(df)
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")

        if dfs:
            new_data = pd.concat(dfs, ignore_index=True)
            master_df = pd.concat([master_df, new_data], ignore_index=True)
            master_df.to_excel(DATA_FILE, index=False)
            st.success("Data added and stored to master Excel file!")

# Download button for merged data
if not master_df.empty:
    st.subheader("Download Master Excel File")
    buffer = BytesIO()
    master_df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button("Download Current Master File", buffer, "master_merged_data.xlsx")
else:
    st.info("No data has been merged yet.")
