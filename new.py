import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Function to perform web search
def perform_web_search(query):
    """
    Perform a web search using Wikipedia as the primary source and Google Search as fallback.
    """
    # Encode the query to handle special characters and spaces
    encoded_query = quote_plus(query)
    target_url = f"https://en.wikipedia.org/wiki/{encoded_query}"

    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            # Parse the Wikipedia page content
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            snippets = [para.text.strip() for para in paragraphs if para.text.strip()]
            
            if snippets:
                return snippets[:3]  # Return the first three snippets
            else:
                st.warning(f"No meaningful information found on Wikipedia for '{query}'.")
                return perform_fallback_search(query)
        else:
            st.warning(f"Wikipedia search failed for '{query}'. Falling back to Google search.")
            return perform_fallback_search(query)
    except Exception as e:
        st.error(f"Error during web search: {e}")
        return ["Error during web search."]

def perform_fallback_search(query):
    """
    Use Google Search for fallback results.
    """
    try:
        encoded_query = quote_plus(query)
        fallback_url = f"https://www.google.com/search?q={encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(fallback_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract search result snippets
            snippets = [
                result.text.strip()
                for result in soup.find_all("span")  # Adjusted class if default is unavailable
            ]
            if snippets:
                return snippets[:3]  # Return top 3 snippets
            else:
                st.warning(f"No snippets found on Google for '{query}'.")
                return ["No fallback results found."]
        else:
            st.warning(f"Google search failed with HTTP Status: {response.status_code}")
            return ["Fallback search failed."]
    except Exception as e:
        st.error(f"Error during fallback search: {e}")
        return ["Error during fallback search."]

# Streamlit App
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
        prompt_template = st.text_input(
            "Enter a custom prompt for information retrieval", "Get the definition of {entity}"
        )

        # Step 4: Process and search
        if st.button("Run Search"):
            results = []

            # Process each entity in the selected column
            for entity in df[main_column].dropna():
                entity_str = str(entity)  # Ensure entity is a string
                prompt = prompt_template.replace("{entity}", entity_str)

                # Perform web search
                search_results = perform_web_search(entity_str)

                if search_results:
                    # Combine prompt and search results for the output
                    extracted_info = f"Prompt: {prompt}\nSearch Results:\n" + "\n".join(search_results)
                    results.append({"Entity": entity_str, "Extracted Information": extracted_info})
                else:
                    results.append({"Entity": entity_str, "Extracted Information": "No results found."})

            # Convert results to a DataFrame and display
            results_df = pd.DataFrame(results)
            st.write("Extracted Information:")
            st.write(results_df)

            # Option to download the results as CSV
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download results as CSV", data=csv, file_name='extracted_information.csv', mime='text/csv'
            )
else:
    st.write("Please upload a CSV file to proceed.")
