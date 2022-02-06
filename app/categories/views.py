# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from .models import Category
from .schemas import CategorySchema

blueprint = Blueprint(
    "categories", __name__, url_prefix="/categories", description="Categories"
)


@blueprint.route("/")
@blueprint.response(200, CategorySchema(many=True))
@jwt_required()
def category_list():
    categories = Category.query.order_by(Category.created)

    return categories
