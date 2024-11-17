import streamlit as st
import pandas as pd
import os
import requests
from dotenv import load_dotenv
import openai

# Load environment variables

SERPAPI_API_KEY = "3fee63c2358a6729ccc3b468cd5e1a6915d1fb59b7107b205b3dd28744d720cf"
OPENAI_API_KEY = "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"

#load_dotenv()
#SERPAPI_API_KEY = os.getenv(SERPAPI_API_KEY)
#OPENAI_API_KEY = os.getenv(OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY




def perform_web_search(query):
    """
    Perform a web search using SerpAPI.
    """
    if not SERPAPI_API_KEY:
        st.error("SerpAPI API key not found. Please check your .env file.")
        return None
    
    params = {
        "api_key": SERPAPI_API_KEY,
        "q": query,
        "num": 5,  # Number of results to fetch
        "engine": "google"  # Use Google search engine
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        search_results = response.json().get("organic_results", [])
        return [result.get("snippet", "") for result in search_results]
    else:
        st.error("Failed to fetch search results.")
        return None


def parse_with_llm(prompt, search_results):
    """
    Use an LLM (OpenAI GPT) to parse search results and extract information.
    """
    if not OPENAI_API_KEY:
        st.error("OpenAI API key not found. Please check your .env file.")
        return "Error: Missing OpenAI API key."
    
    # Format the content to send to the LLM
    formatted_content = f"{prompt}\n\nWeb Search Results:\n" + "\n".join(search_results)
    
    try:
        # Use OpenAI's ChatCompletion API to process the prompt and search results
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts specific information."},
                {"role": "user", "content": formatted_content}
            ],
            max_tokens=100,
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return "Error in extraction."



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
    
    if main_column:
        st.write(f"You selected the '{main_column}' column.")
        
        # Step 3: Input for Custom Prompt
        prompt_template = st.text_input("Enter a custom prompt for information retrieval", "Get the email address of {entity}")
        
        # Placeholder button for running search
        if st.button("Run Search"):
            results = []
            
            # Step 4: Process each entity in the selected column
            for entity in df[main_column].dropna():
                # Replace placeholder with actual entity in the prompt
                prompt = prompt_template.replace("{entity}", entity)
                
                # Perform web search with SerpAPI
                search_results = perform_web_search(entity)
                
                if search_results:
                    # Pass results to LLM for extraction
                    extracted_info = parse_with_llm(prompt, search_results)
                    results.append({"Entity": entity, "Extracted Information": extracted_info})
                else:
                    results.append({"Entity": entity, "Extracted Information": "No results found"})
            
            # Convert results to a DataFrame and display
            results_df = pd.DataFrame(results)
            st.write("Extracted Information:")
            st.write(results_df)
            
            # Option to download the results as CSV
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download results as CSV", data=csv, file_name='extracted_information.csv', mime='text/csv')
else:
    st.write("Please upload a CSV file to proceed.")
