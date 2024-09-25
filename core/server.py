from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from json import load
from core.models import *
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources,principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from os import listdir
app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')

@app.route('/')
def ready():
    dir_path="core/"
    file_list=listdir(dir_path)
    if("data.json" in file_list):
        db.drop_all()
        db.create_all()
        data=load(open("data.json")
                  )
        for i in data:
            for j in data[i]:
                person=User(username=j["username"],email=j["email"])
                if(i=="teacher"):
                    teach_=Teacher(user=person)
                    db.session.add_all([person,teach_])
                elif(i=="student"):
                    student=Student(user=person)
                    db.session.add_all([person,student])
                else:
                    principal=Principal(user=person)
                    db.session.add_all([person,principal])
        db.session.commit()
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)+" or data already Exist"
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err
