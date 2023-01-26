from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import SizeController
from .builder_services import ServiceBuilder

class SizeServiceBuilder(ServiceBuilder):
    controller = SizeController
    name = 'size'
    import_name = __name__

size = SizeServiceBuilder.build()


