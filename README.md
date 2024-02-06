# University of Adelaide Course Guide API

## Overview
This repository contains the API for the [University of Adelaide Course Guide GPT](https://chat.openai.com/g/g-E2mWxfcoJ-university-of-adelaide-course-guide), an AI-powered guide that helps users select courses at the University of Adelaide. The API, built with Flask, interfaces with a SQLite database to manage and provide detailed information about university courses. It is an integral part of the system, enabling the GPT to access up-to-date course data through structured endpoints.

## Features
- RESTful API for querying university courses and subjects.
- Integration with a SQLite database for persistent storage of course information.
- Custom web scraping script (`webParser.py`) for extracting and updating course data.
- OpenAPI specification for clear API documentation.
- Plugin manifest (`ai-plugin.json`) included for broader system integration.

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
3. Initialize the SQLite database (if not already done):
   ```
   python setup_database.py  # Replace with your actual database setup script
   ```

## Running the Application
Start the application with:
```
python app.py
```
This command launches the Flask server, making the API accessible for the University of Adelaide Course Guide GPT.

## API Endpoints
The following endpoints are critical for the GPT to function effectively:
- `GET /UoA/subjects`: Lists distinct subjects available.
- `GET /UoA/courses/<subject>/<level>`: Retrieves courses based on subject and level.
- `GET /UoA/courses/<course_code>`: Provides details for a specific course.
- Endpoints for serving plugin assets like logo, OpenAPI spec, and plugin manifest.

## Web Parser
The `webParser.py` script scrapes course data from specified URLs for database updates. It's pivotal for maintaining current course information.

## Configuration Files
- `ai-plugin.json`: Describes the API for integration with external systems.
- `openapi.yaml`: Documents the API endpoints and their specifications.

## Integration with [University of Adelaide Course Guide GPT](https://chat.openai.com/g/g-E2mWxfcoJ-university-of-adelaide-course-guide)
This API is designed to work in tandem with the [University of Adelaide Course Guide GPT](https://chat.openai.com/g/g-E2mWxfcoJ-university-of-adelaide-course-guide). It provides the necessary backend support for the AI model to deliver accurate and up-to-date course information to users.

### Examples
![image](https://github.com/jackdrowlands/courseHelperAPI/assets/119843072/ca25e355-c7be-47e6-a9bf-20a667dc9b75)
![image](https://github.com/jackdrowlands/courseHelperAPI/assets/119843072/3d887296-d8c2-4c61-9c77-10b1ee9ae7bb)
![image](https://github.com/jackdrowlands/courseHelperAPI/assets/119843072/42f4021e-3b83-4a5c-a892-6d4f965c399b)
![image](https://github.com/jackdrowlands/courseHelperAPI/assets/119843072/280b6d3f-f7b7-424e-81b8-8843a0062648)


## Disclaimer
This API is not officially endorsed by the University of Adelaide. It is a student project  and is not intended for commercial use.
