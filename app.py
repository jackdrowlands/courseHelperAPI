from flask import Flask, jsonify, request
import sqlite3
from flask import send_file, send_from_directory
import yaml
import os


app = Flask(__name__)

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('university_courses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to close database connection
def close_db_connection(conn):
    conn.close()

import re

def get_subject(course_code):
    match = re.match(r'(.*?)(?=\d)', course_code)
    return match.group(1).strip() if match else None

# Register the function with SQLite
sqlite3.enable_callback_tracebacks(True)
sqlite3.connect(':memory:').create_function('get_subject', 1, get_subject)

@app.route('/UoA/subjects', methods=['GET'])
def get_subjects():
    conn = get_db_connection()
    conn.create_function('get_subject', 1, get_subject)
    subjects = conn.execute(
        'SELECT DISTINCT get_subject(course_code) as subject FROM courses'
    ).fetchall()
    close_db_connection(conn)
    
    # Create a list of subjects
    subject_list = [subject['subject'] for subject in subjects]
    
    return jsonify(subject_list)


@app.route('/UoA/courses/<string:subject>/<string:level>', methods=['GET'])
def get_courses(subject, level):
    conn = get_db_connection()
    conn.create_function('get_subject', 1, get_subject)
    # Concatenate course_code and course_name in the query
    courses = conn.execute(
        'SELECT DISTINCT course_code || " - " || course_name as course_full_name FROM courses WHERE get_subject(course_code) = ? AND level = ?',
        (subject, level,)
    ).fetchall()
    close_db_connection(conn)
    
    # Create a list of course names
    course_list = [course['course_full_name'] for course in courses]
    
    return jsonify(course_list)



@app.route('/UoA/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    conn = get_db_connection()
    course = conn.execute(
        'SELECT * FROM courses WHERE course_code = ?',
        (course_code,)
    ).fetchall()
    close_db_connection(conn)
    # check if more than one course is returned
    # if it is, conjoin the terms
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    if len(course) > 1:
        terms = [course['term'] for course in course]
        course_dict = dict(course[0])  # Convert the sqlite3.Row object to a dictionary
        course_dict['term'] = ', '.join(terms)
        course = [course_dict]  # Replace the list of sqlite3.Row objects with a list of dictionaries
    # check if course is empty
    return jsonify([dict(row) for row in course])


@app.get("/logo.png")
async def plugin_logo():
  filename = 'logo.png'
  return send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
def serve_manifest():
    return send_from_directory(os.path.dirname(__file__), 'ai-plugin.json')

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        # Have to make it json serializable
        print(jsonify(yaml.load(text)))
        return jsonify(yaml.load(text))

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, ssl_context=('/workspaces/courseHelperAPI/cert.pem', '/workspaces/courseHelperAPI/key.pem'))
