from flask_restful import Resource, reqparse
from app.models.expense import Expense
from app.extensions import db

class ExpenseResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True, help="Title is required")
    parser.add_argument("amount", type=float, required=True, help="Amount is required")
    parser.add_argument("date", type=str, required=True, help="Date is required (YYYY-MM-DD)")
    parser.add_argument("user_id", type=int, required=True, help="User ID is required")

    def get(self, expense_id=None):
        if expense_id:
            expense = Expense.query.get(expense_id)
            if not expense:
                return {"message": "Expense not found"}, 404
            return {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "date": expense.date.strftime("%Y-%m-%d"),
                "user_id": expense.user_id
            }, 200
        expenses = Expense.query.all()
        return [
            {
                "id": exp.id,
                "title": exp.title,
                "amount": exp.amount,
                "date": exp.date.strftime("%Y-%m-%d"),
                "user_id": exp.user_id
            } for exp in expenses
        ], 200

    def post(self):
        data = self.parser.parse_args()
        expense = Expense(
            title=data["title"], amount=data["amount"], date=data["date"], user_id=data["user_id"]
        )
        db.session.add(expense)
        db.session.commit()
        return {"id": expense.id, "title": expense.title, "amount": expense.amount}, 201

    def delete(self, expense_id):
        expense = Expense.query.get(expense_id)
        if not expense:
            return {"message": "Expense not found"}, 404
        db.session.delete(expense)
        db.session.commit()
        return {"message": f"Expense {expense_id} deleted"}, 200
