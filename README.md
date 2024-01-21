# University Courses Helper API

## Overview
The University Courses Helper API is a Flask-based web application designed to manage and provide information about university courses. This application allows users to view course details, access specific course information by course code, and manage course data effectively. It features a RESTful API, a SQLite database for course data storage, and a web parser for extracting course information from specified URLs.

## Features
- REST API to query university courses and subjects.
- SQLite database integration for storing course information.
- Customizable web scraping script for extracting course data.
- OpenAPI specification for API documentation.
- Plugin manifest (`ai-plugin.json`) for integration with external systems.

## Installation

### Prerequisites
- Python 3.x
- Flask
- SQLite3
- Additional Python libraries: `requests`, `BeautifulSoup`, `yaml`, `re`, `urllib3`

### Setup
1. Clone the repository:
   ```
   git clone [repository URL]
   ```
2. Install the required Python libraries:
   ```
   pip install flask sqlite3 requests beautifulsoup4 pyyaml urllib3
   ```
3. Run the `webParser.py` script to scrape course data from specified URLs and store it in the database:
   ```
    python webParser.py
    ```

## Running the Application
To run the application, execute the following command:
```
python app.py
```
This will start the Flask server, making the API accessible at `http://localhost:5000`.

## API Endpoints
- `GET /UoA/subjects`: Fetches a list of distinct subjects.
- `GET /UoA/courses/<subject>/<level>`: Retrieves courses based on the subject and level.
- `GET /UoA/courses/<course_code>`: Gets details of a specific course by course code.
- Additional endpoints for serving the plugin logo, OpenAPI specification, and plugin manifest.

## Web Parser Usage
The `webParser.py` script is used for scraping course data from specified URLs and storing it in the database. Modify the `urls_to_scrape` list as needed for different sources.

## Configuration Files
- `ai-plugin.json`: Plugin manifest for external integration.
- `openapi.yaml`: OpenAPI specification for API documentation.