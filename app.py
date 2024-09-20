import streamlit as st
import pandas as pd
import json
import os

# Function to extract relevant fields from a user payload
def process_user(user):
    user_info = {
        "id": user.get("id"),
        "name": user.get("name"),
        "bio": user["metadata"].get("bio"),
        "chatRequest": user["metadata"].get("chatRequest"),
        "lastOffline": user["metadata"].get("lastOffline"),
        "online": user["metadata"].get("online"),
        "pictureProfile": user["metadata"].get("pictureProfile"),
        "pictureBubble": user["metadata"].get("pictureBubble"),
        "spData": user["metadata"].get("spData"),
        "createdAt": user.get("createdAt"),
        "updatedAt": user.get("updatedAt"),
        "email": user.get("email"),
        "firstName": user.get("firstName"),
        "lastName": user.get("lastName"),
        "role": user["member"].get("role"),
        "memberId": user["member"].get("id"),
        "userId": user["member"].get("userId"),
        "groupId": user["member"].get("groupId"),
        "requestedAt": user["member"]["metadata"].get("requestedAt"),
        "memberCreatedAt": user["member"].get("createdAt"),
        "memberUpdatedAt": user["member"].get("updatedAt"),
        "approvedAt": user["member"].get("approvedAt"),
        "lastOfflineMember": user["member"].get("lastOffline")
    }
    return user_info

# Function to load all JSON files and process data
def load_and_process_files(files):
    all_users = []
    for file in files:
        # Load the JSON data from each file
        data = json.load(file)
        # Extract the user data
        users_data = data.get("pageProps", {}).get("users", [])
        # Process each user and append to the list
        for user in users_data:
            all_users.append(process_user(user))
    return all_users

# Streamlit app UI
st.title("User Information Database")

# Upload multiple JSON files
uploaded_files = st.file_uploader("Upload JSON Files", accept_multiple_files=True, type=["json"])

if uploaded_files:
    # Process all uploaded files
    all_user_data = load_and_process_files(uploaded_files)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_user_data)
    
    # Display the DataFrame with sorting and filtering options
    st.dataframe(df)
    
    # Provide an option to download the data as a CSV
    csv = df.to_csv(index=False)
    st.download_button("Download Data as CSV", csv, "users_data.csv", "text/csv")
