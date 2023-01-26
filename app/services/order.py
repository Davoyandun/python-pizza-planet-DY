from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request

from ..controllers import OrderController
from .builder_services import ServiceBuilder

class OrderServiceBuilder(ServiceBuilder):
    controller = OrderController
    service = 'order'

order = OrderServiceBuilder.build()