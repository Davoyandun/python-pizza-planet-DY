from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import BeverageController
from .builder_services import ServiceBuilder

class BeverageServiceBuilder(ServiceBuilder):
    controller = BeverageController
    service = 'beverage'


beverage = BeverageServiceBuilder.build()