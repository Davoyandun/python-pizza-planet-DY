from flask import Blueprint, jsonify, request
from app.controllers.base import BaseController
from app.common.http_methods import GET, POST, PUT


class ServiceBuilder:
    result: Blueprint = None
    controller: BaseController = None
    service: str = None

    @classmethod
    def build_create_route(cls):
        def create_method():
            item, error = cls.controller.create(request.json)
            response = item if not error else {'error': error}
            status_code = 200 if not error else 400
            return jsonify(response), status_code

        cls.result.add_url_rule('/', view_func=create_method, methods=POST)

    @classmethod
    def build_update_route(cls):
        def update_method(_id: int):
            item, error = cls.controller.update({"_id": _id} | request.json)
            response = item if not error else {'error': error}
            status_code = 200 if not error else 400
            return jsonify(response), status_code

        cls.result.add_url_rule('/', view_func=update_method, methods=PUT)

    @classmethod
    def build_get_by_id_route(cls):
        def get_by_id_method(_id: int):
            item, error = cls.controller.get_by_id(_id)
            response = item if not error else {'error': error}
            status_code = 200 if item else 404 if not error else 400
            return jsonify(response), status_code

        cls.result.add_url_rule(
            '/id/<_id>', view_func=get_by_id_method, methods=GET
        )

    @classmethod
    def build_get_all_route(cls):
        def get_all_method():
            items, error = cls.controller.get_all()
            response = items if not error else {'error': error}
            status_code = 200 if items else 404 if not error else 400
            return jsonify(response), status_code

        cls.result.add_url_rule('/', view_func=get_all_method, methods=GET)

    @classmethod
    def build_blueprint(cls):
        cls.result = Blueprint(cls.service, cls.service)

    @classmethod
    def build(cls):
        cls.build_blueprint()
        cls.build_create_route()
        cls.build_update_route()
        cls.build_get_by_id_route()
        cls.build_get_all_route()

        return cls.result