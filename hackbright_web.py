"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            projects=projects)

    return html


@app.route("/student-search")
def search_for_student():
    """show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/create-student")
def show_student_creation_form():
    """Show form for creating a new student."""

    return render_template("create_student.html")


@app.route("/api/create-student", methods=["POST"])
def create_student():
    """Get values from form and save new student in database."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("confirmation_template.html", first=first_name,
                                                            last=last_name,
                                                            github=github)

@app.route("/create-project")
def show_project_creation_form():
    """Displays form for user to complete to create a new project."""

    return render_template("create_project.html")


@app.route("/api/create-project", methods=["POST"])
def create_project():
    "Get values from form and save new project in database."

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_confirmation.html", title=title)

@app.route("/project")
def show_project_details():
    """Show details of a project along with students and their grades
    on the project."""

    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)

    student_grades = hackbright.get_grades_by_title(title)

    return(render_template("project_details.html", title=title,
                                                    description=description,
                                                    max_grade=max_grade,
                                                    student_grades=student_grades))


@app.route("/homepage")
def show_homepage():
    """Display homepage which lists all students and all projects."""

    students = hackbright.get_all_students()

    projects = hackbright.get_all_projects()

    return(render_template("homepage.html", students=students,
                                            projects=projects))


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
