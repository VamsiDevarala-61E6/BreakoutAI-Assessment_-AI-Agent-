import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the title of the app
st.title("AI Agent Dashboard")

# Step 1: Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display a preview of the data
    st.write("Data Preview:")
    st.write(df.head())
    
    # Step 2: Select the main column to process
    columns = df.columns.tolist()
    main_column = st.selectbox("Select the main column for processing", columns)
    
    # Ensure that a main column is selected before showing the prompt input
    if main_column:
        st.write(f"You selected the '{main_column}' column.")
        
        # Step 3: Input for Custom Prompt
        prompt = st.text_input("Enter a custom prompt for information retrieval", "Get the email address of {entity}")
        
        # Display the user's prompt
        st.write("Your custom prompt:", prompt)
        
        # Placeholder button for running search
        if st.button("Run Search"):
            # Placeholder output for search results
            st.write("Search results will be displayed here.")
else:
    st.write("Please upload a CSV file to proceed.")
