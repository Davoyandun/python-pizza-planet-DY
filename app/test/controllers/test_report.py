import pytest

from app.controllers import ReportController, OrderController


def test_report_get_all(app, order):
    _, error_order = OrderController.create(order)
    report, error = ReportController.get_report()
    pytest.assume(error is None)
    pytest.assume(error_order is None)
    pytest.assume(report.get('top_ingredient'))
    pytest.assume(report.get('top_beverage'))
    pytest.assume(report.get('top_month'))
    pytest.assume(report.get('top3_clients'))

