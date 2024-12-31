from flask_restful import Resource, reqparse
from app.models.user import User
from app.extensions import db

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username is required")
    parser.add_argument("email", type=str, required=True, help="Email is required")

    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return {"id": user.id, "username": user.username, "email": user.email}, 200
        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email": user.email} for user in users], 200

    def post(self):
        data = self.parser.parse_args()
        user = User(username=data["username"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        return {"id": user.id, "username": user.username, "email": user.email}, 201

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user_id} deleted"}, 200
