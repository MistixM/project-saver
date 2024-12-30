from flask import Flask, jsonify, request, render_template, redirect

from utils.db import register_project, get_projects, delete_project, update_project, project_exists
from utils.generate_token import generate_token
from utils.auth import requires_auth, get_session_token

app = Flask(__name__)
app.secret_key = get_session_token()

@app.route('/', methods=['POST', 'GET'])
@requires_auth
def index():
    error = None

    if request.method == "POST":
        project_name = request.form['project_name']

        if project_name:
            token = generate_token()

            # Register the project in the database
            if not project_exists(project_name):
                register_project(project_name, token)
                return redirect('/')

            else:
                error = "Project already exists"

        else:
            error = "Please enter a project name"
            
    # Get task info from the database here
    projects = get_projects()

    return render_template('index.html', projects=projects, error_messages=error)
    
@app.route('/delete/<string:project_name>', methods=['POST'])
@requires_auth
def delete(project_name):
    delete_project(project_name)
    return redirect('/')

@app.route('/update/<string:project_name>', methods=['POST', 'GET'])
@requires_auth
def update_api(project_name):
    token = generate_token()

    update_project(project_name, {"api": token})
    
    return redirect('/')

# API methods
@app.route('/request_access', methods=['POST'])
def handle_request():
    data = request.get_json()

    # If request contains invalid parameters, refuse access
    if not data or 'api' not in data:
        return jsonify({"status": "error", "message": "Invalid request"}), 400
    
    # Check each project in the database
    projects = get_projects()

    # Check each project api
    for project in projects:
        if data['api'] == project['api']:
            return jsonify({"status": "success", "message": "Access granted"}), 200
    else:
        return jsonify({"status": "error", "message": "Project does not exist"}), 403

if __name__ == '__main__': 
    app.run(debug=True)