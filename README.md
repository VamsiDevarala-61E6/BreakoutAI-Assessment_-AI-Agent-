# BreakoutAI-Assessment_-AI-Agent-

![image](https://github.com/user-attachments/assets/2817eff2-62fb-4b70-9392-fdcecc5a8cc3)
![image](https://github.com/user-attachments/assets/0d3b0a5c-e879-46dd-b2f2-cf3b42c23985)

Steps to Use This Code
Install Dependencies: Before running the code, make sure you have the required libraries installed. Run the following command in your terminal:



pip install streamlit pandas requests beautifulsoup4
Save the Code: Save the code into a Python file, e.g., search_app.py.

Run the Streamlit App: In your terminal, navigate to the folder where search_app.py is saved and run:



streamlit run search_app.py
Upload the CSV File:

Once the app is running, you will see a file uploader. Upload a CSV file containing entities in one column (e.g., "AIML", "Python").
Ensure the CSV has a proper header row. For example:
Entity
AIML
Python
Streamlit
Select the Column to Process:

After uploading the file, select the column containing the entities.
Customize the Prompt:

Enter a custom prompt, such as "Find the definition of {entity}."
The app will replace {entity} with each term from the selected column during the search.
Run the Search:

Click the "Run Search" button. The app will retrieve the top 3 snippets for each entity from Wikipedia or Google.
View and Download Results:

The results will be displayed in a table.
You can download the extracted information as a CSV file by clicking the "Download results as CSV" button.
Dependencies Needed
Here’s a list of the required Python libraries:

Streamlit:

Framework for building web apps in Python.
Install using pip install streamlit.
Pandas:

Used for reading and processing the CSV file.
Install using pip install pandas.
Requests:

For making HTTP requests to Wikipedia and Google.
Install using pip install requests.
BeautifulSoup4:

For parsing HTML content from Wikipedia and Google search results.
Install using pip install beautifulsoup4.
Additional Notes
CSV Format: The CSV file must include a column with headers. For example:

csv
Entity
AIML
Python
Streamlit
User-Agent for Google Search: The code uses a user-agent header for Google search to mimic a browser request. Ensure your internet connection allows access to Google Search and Wikipedia.

Error Handling: If a search fails (e.g., Wikipedia doesn't have results), the app falls back to Google or provides a meaningful error message.

Running Locally: The app runs on your localhost, and you'll see its output in your default web browser.
