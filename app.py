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

# Ensure the database is initialized

@app.route('/UoA/courses/<string:level>', methods=['GET'])
def get_courses(level):
    conn = get_db_connection()
    # Concatenate course_code and course_name in the query
    courses = conn.execute(
        'SELECT DISTINCT course_code || " - " || course_name as course_full_name FROM courses WHERE level = ?',
        (level,)
    ).fetchall()
    close_db_connection(conn)
    
    # Create a list of course names
    course_list = [course['course_full_name'] for course in courses]
    
    return jsonify(course_list)


@app.route('/UoA/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    try:
        conn = get_db_connection()
        # Ensure the course_code is correctly formatted
        # For example, replace any URL-encoded spaces (%20) with actual spaces
        formatted_course_code = course_code.replace('%20', ' ')
        
        # Fetch all courses with the given course_code
        courses = conn.execute(
            'SELECT * FROM courses WHERE course_code = ?',
            (formatted_course_code,)
        ).fetchall()
        close_db_connection(conn)
    except Exception as e:
        return jsonify({'message': 'Database error: ' + str(e)}), 500

    if courses:
        # Convert each course row to a dictionary
        courses_info = [dict(course) for course in courses]

        # If there are multiple courses with the same code, concatenate their term fields
        if len(courses_info) > 1:
            terms = ', '.join(course['term'] for course in courses_info)
            course_info = {**courses_info[0], 'term': terms}
        else:
            course_info = courses_info[0]

        return jsonify(course_info)
    else:
        return jsonify({'message': 'Course not found'}), 404




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
