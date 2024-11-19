# Entity Info Extractor

Overview
This Python-based application extracts specific information about entities such as companies, people, or products by:
Fetching data from Google Search using the SerpAPI.
Cleaning the search results.
Extracting relevant details via the Groq API using a machine learning model.
The application provides options to either upload a CSV file or link a Google Spreadsheet as the input data source. It also includes robust error handling, including retries for failed API calls, and notifies the user about errors during processing.

## Loom Video Link:
https://drive.google.com/file/d/1Gq-zAl0UVdiGtg63lr4DxcC0Z5dvXr9i/view?usp=sharing
## Project Structure

- **app.py**: The main file to run the Streamlit app, allowing users to upload CSVs or link a Google Sheet. It interacts with the Google Sheets API to read/write data.
- **agent.py**: Implements the `TaskManager` class which handles task execution with retries and logging retries any failure like api call failure for three times with delay of 5 secs.
- **fetch_data.py**: Fetches search results from Google Search using the SerpAPI.
- **clean_data.py**: Cleans the raw search results JSON to remove unnecessary data.
- **extract_info_mo.py**: Extracts specific information using the Groq API.
- **.env**: Contains environment variables such as API keys (Google API key and Groq API key).
- **requirements.txt**: Contains the Python dependencies required for the project.
- **credentials.json**: credentials of google cloud console application to acess and manage spreadsheet api and provide authorisation.
  
## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akshat-agr/Data_Extraction_Akshat_AGRAWAL.git

### 2.Run
    
    pip install -r requirements.txt

### 3. Setup serpapi and grooq api key through registering on their websites .
   - create a .env file in this format
   - google_api_key = "#your serpapi key"
   - groq_api_key = "#your groq api key"


### 4. Create a Project in [Google Cloud Console](https://console.cloud.google.com/)

- Enable the Google Sheets API.
- Set up the OAuth consent screen with external users.
- Create OAuth 2.0 credentials and download the `credentials.json` file.
- Place the `credentials.json` file in the root directory of the project.


5. Run the streamlit app using
   ```bash
   streamlit run app.py

## Key Features

**Flexible Input Options:**
- Upload a CSV file containing entity data.
- Link a Google Sheet by providing its Sheet ID.

**Data Fetching and Cleaning:**
- Uses Google Search (via SerpAPI) to fetch information.
- Cleans search results to retain only relevant data.

**Machine Learning-Powered Extraction:**
- Uses Groq API for precise extraction of the requested information.
- **Allows Multiple Fields Info in Single Prompt:** Retrieve multiple data points (e.g., "CEO" and "Revenue") in a single query.

**Error Handling:**
- Automatically retries API calls on failure.
- Logs errors and provides user-friendly notifications.

## External APIs Used

### 1. Google Cloud Console
**Google Sheets API**  
- **Purpose:** To interact with Google Sheets for reading and updating spreadsheet data.  
- **Description:** Allows seamless integration with Google Sheets. The application can read data from a specified sheet, process it, and write back the updated data.

### 2. SerpAPI (Google Search API)
- **Purpose:** To fetch search results for specific entities and requested information.  
- **Description:** Provides a simple way to scrape Google Search results in real time. Returns structured JSON data, making it easy to extract relevant search results.  

**Key Features:**
- High accuracy in fetching search results.
- Ability to filter results such as top organic listings.

**Usage in Application:**
- Queries Google Search for a combination of the entity and the required information (e.g., "Tesla CEO").

### 3. Groq API
- **Purpose:** To extract specific information from cleaned search results using machine learning models.  
- **Description:** Provides advanced natural language processing capabilities. It can accurately extract requested details from unstructured text using pre-trained machine learning models.

**Key Features:**
- High precision in extracting targeted information from large text datasets.
- Supports customizable queries for extracting specific entity information.

**Usage in Application:**
- After fetching and cleaning data, the application uses Groq API to extract details like "CEO" or "Revenue" from the results.





  


  
   
