from app.common.http_methods import GET
from flask import Blueprint, jsonify

from app.controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    report, error = ReportController.get_report()
    response = report if not error else {'error': error}
    print(response)
    status_code = 200 if not error else 400
    return jsonify(response), status_code