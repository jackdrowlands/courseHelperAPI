# University Courses Manager - Vercel Branch

## Overview
This branch of the University Courses Manager project is tailored for deployment on Vercel, a cloud platform for static sites and Serverless Functions. It includes specific configurations and optimizations for running the Flask-based university course management application on Vercel.

## Features
- Optimized for deployment on Vercel with custom configurations.
- RESTful API for university course and subject management.
- Integration with a SQLite database for persistent data storage.
- Adapted workflow for Vercel's serverless environment.

## Prerequisites
- Vercel account and Vercel CLI installed.
- Python 3.x and required Python libraries from the `requirements.txt` file.

## Setup and Deployment
### Local Setup
1. Clone the repository and switch to the Vercel branch:
   ```
   git clone [repository URL]
   git checkout vercel-branch
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Vercel Deployment
1. Initialize your project with Vercel by running:
   ```
   vercel
   ```
2. Follow the prompts to link your project and set up environment variables as needed.

3. Deploy your application:
   ```
   vercel --prod
   ```

## Environment Variables
- `DATABASE_PATH`: Set the path to your SQLite database file. For example, `/path/to/university_courses.db`.

## API Endpoints
- (List all the API endpoints as in the main branch README, highlighting any changes if applicable.)

## Notes for Vercel Deployment
- Ensure that the Flask application is configured to run in a serverless environment.
- Be aware of Vercel's serverless function execution limits and pricing.

## Local Development
For local development, you can use the Vercel CLI:
```
vercel dev
```
This command will emulate the Vercel environment on your local machine.

## Additional Resources
- Vercel Documentation: [Vercel Docs](https://vercel.com/docs)
