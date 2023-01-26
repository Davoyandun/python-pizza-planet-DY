from flask import request, jsonify
from app.common.http_methods import PUT
from ..controllers import IngredientController
from .builder_services import ServiceBuilder


class IngredientServiceBuilder(ServiceBuilder):
    controller = IngredientController
    service = 'ingredient'

ingredient = IngredientServiceBuilder.build()