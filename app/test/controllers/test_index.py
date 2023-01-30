import pytest

from app.controllers import IndexController


def test_connection(app):
    response, error = IndexController.test_connection()
    pytest.assume(response is True)
    pytest.assume(error == '')
