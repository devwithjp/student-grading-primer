from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

def error_response(message):
    return jsonify({"error": message}), 404


def _request_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")
    return data


def _required_text(data, field):
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


def _optional_mark(data):
    if "mark" not in data or data.get("mark") in (None, ""):
        return None
    try:
        mark = int(data["mark"])
    except (TypeError, ValueError):
        raise ValueError("mark must be an integer")
    if mark < 0 or mark > 100:
        raise ValueError("mark must be between 0 and 100")
    return mark


@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    try:
        student_data = _request_body()
        name = _required_text(student_data, "name")
        course = _required_text(student_data, "course")
        mark = _optional_mark(student_data)
        student = db.insert_student(name, course, mark)
    except ValueError as e:
        return error_response(str(e))

    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = _request_body()
        name = _required_text(student_data, "name")
        course = _required_text(student_data, "course")
        mark = _optional_mark(student_data)
        student = db.update_student(student_id, name=name, course=course, mark=mark)
    except ValueError as e:
        return error_response(str(e))

    if student is None:
        return error_response("Student not found")

    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)
    if deleted is None:
        return error_response("Student not found")

    return jsonify(deleted), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    marks = [
        student["mark"]
        for student in db.get_all_students()
        if isinstance(student.get("mark"), int)
    ]
    if not marks:
        return jsonify({"count": 0, "average": 0, "min": None, "max": None}), 200

    return jsonify({
        "count": len(marks),
        "average": round(sum(marks) / len(marks), 2),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
