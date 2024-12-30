from firebase_admin import credentials
from firebase_admin import db

import firebase_admin

cred = credentials.Certificate('constants/firestore-config.json')
firebase_admin.initialize_app(cred, {'databaseURL': "https://project-saver-883db-default-rtdb.europe-west1.firebasedatabase.app/"})

proj_ref = db.reference('projects')

def register_project(project_name, api_key):
    data = {
        "api": api_key
    }

    proj_ref.child(project_name).set(data)

def project_exists(project_name):
    return proj_ref.child(project_name).get()

def get_projects() -> list:
    projects = proj_ref.get()
    project_list = []

    if projects:
        for project_name, project_api in projects.items():
            project_list.append({
                "name": project_name,
                "api": project_api.get('api')
            })

    return project_list

def delete_project(project_name) -> None:
    proj_ref.child(project_name).delete()

def update_project(project_name, value) -> None:
    proj_ref.child(project_name).update(value)

