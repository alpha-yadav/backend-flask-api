from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)
@principal_assignments_resources.route("/assignments",methods=("GET",))
@decorators.authenticate_principal
def set_assignment(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
@principal_assignments_resources.route("/teachers",methods=("GET",))
@decorators.authenticate_principal
def list_teacher(p):
    """LIST OF ALL TEACHERS """
    teach_list=Teacher.get_list()
    res_list=AssignmentSchema().dump(teach_list,many=True)
    return APIResponse.respond(data=res_list)
@principal_assignments_resources.route("/assignments/grade",methods=("POST",))
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p,incoming_payload):
        """Grade or Regrade an assignment"""
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
        graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
        )
        print(p)
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
