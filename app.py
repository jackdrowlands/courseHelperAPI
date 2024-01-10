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

@app.route('/UoA/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT title FROM courses').fetchall()
    close_db_connection(conn)
    return jsonify([dict(course) for course in courses])

# @app.route('/courses', methods=['POST'])
# def create_course():
    course = request.json
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO courses (title, course_code, course_name, course_description) VALUES (?, ?, ?, ?)', 
                          (course['title'], course['course_code'], course['course_name'], course['course_description']))
    conn.commit()
    new_course_id = cursor.lastrowid
    close_db_connection(conn)
    course['id'] = new_course_id
    return jsonify(course), 201

@app.route('/UoA/courses/<string:course_code>', methods=['GET'])
def get_course(course_code):
    conn = get_db_connection()
    course = conn.execute('SELECT * FROM courses WHERE course_code = ?', (course_code,)).fetchone()
    close_db_connection(conn)
    if course:
        return jsonify(dict(course))
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
  app.run(host='0.0.0.0', debug=True)
