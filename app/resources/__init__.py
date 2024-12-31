from flask_restful import Api
from .user_resource import UserResource
from .expense_resource import ExpenseResource

api = Api()

def initialize_api(app):
    api.add_resource(UserResource, "/api/users", "/api/users/<int:user_id>")
    api.add_resource(ExpenseResource, "/api/expenses", "/api/expenses/<int:expense_id>")
    api.init_app(app)
