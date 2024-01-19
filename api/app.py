from flask import Flask, jsonify, request, send_file, send_from_directory
import sqlite3
import yaml
import os
import re
from contextlib import closing
from urllib.parse import unquote

app = Flask(__name__)

# Database configuration: Get the database path from environment variable or use default
DATABASE = os.getenv('DATABASE_PATH', 'api/university_courses.db')

def get_subject(course_code):
    """
    Extracts the subject part from a course code using regular expression.
    Example: For 'MATH 1001', it returns 'MATH'.
    """
    match = re.match(r'(.*?)(?=\d)', course_code)
    return match.group(1).strip() if match else None

def get_db_connection():
    """
    Creates and returns a database connection.
    The custom function 'get_subject' is registered for use in SQL queries.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.create_function('get_subject', 1, get_subject)  # Register the function here
    return conn

# Register the custom function with the database connection in the app context
with app.app_context():
    sqlite3.enable_callback_tracebacks(True)
    with get_db_connection() as conn:
        conn.create_function('get_subject', 1, get_subject)

@app.route('/UoA/subjects', methods=['GET'])
def get_subjects():
    """
    API endpoint to get a list of distinct subjects.
    """
    with get_db_connection() as conn:
        subjects = conn.execute(
            'SELECT DISTINCT get_subject(course_code) as subject FROM courses'
        ).fetchall()
    return jsonify([subject['subject'] for subject in subjects])

@app.route('/UoA/courses/<string:subject>/<string:level>', methods=['GET'])
def get_courses(subject, level):
    """
    API endpoint to get courses based on subject and level.
    """
    subject = unquote(subject)
    level = unquote(level)
    with get_db_connection() as conn:
        courses = conn.execute(
            'SELECT DISTINCT course_code || " - " || course_name as course_full_name FROM courses WHERE get_subject(course_code) = ? AND level = ?',
            (subject, level)
        ).fetchall()
    return jsonify([course['course_full_name'] for course in courses])

@app.route('/UoA/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    """
    API endpoint to get details of a specific course.
    """
    course_code = unquote(course_code)
    with get_db_connection() as conn:
        course = conn.execute(
            'SELECT * FROM courses WHERE course_code = ?',
            (course_code,)
        ).fetchall()
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    if len(course) > 1:
        terms = [c['term'] for c in course]
        course_dict = dict(course[0])
        course_dict['term'] = ', '.join(terms)
        course = [course_dict]
    return jsonify([dict(row) for row in course])

@app.get("/logo.png")
async def plugin_logo():
    """
    Endpoint to serve the logo image.
    """
    filename = 'api/logo.png'
    return send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
def serve_manifest():
    """
    Endpoint to serve the ai-plugin.json file.
    """
    file = os.path.abspath(__file__)
    return send_from_directory(os.path.dirname(file), 'ai-plugin.json')

@app.get("/openapi.yaml")
async def openapi_spec():
    """
    Endpoint to serve the OpenAPI specification.
    Replaces the placeholder with the actual host in the spec.
    """
    host = request.headers['Host']
    with open("api/openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        spec = yaml.safe_load(text) # Use safe_load for security
    return jsonify(spec)

@app.route('/')
def home():
    return 'Course Helper API'