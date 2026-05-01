from flask import render_template
import argparse
import os
from flask import Flask, request, jsonify
from db import init_db, get_connection
from accounts import add_account, list_accounts, delete_account
from transactions import add_transaction, list_transaction, delete_transaction
from categories import add_category, list_categories
from budgets import set_budget, list_budgets
from reports import monthly_summary


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/accounts", methods=['GET'])
def get_accounts():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM accounts").fetchall()
    con.close()
    return jsonify([dict(row) for row in rows])


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.json
    name = data['name']
    type = data['type']
    balance = data['balance']
    add_account(name, type, balance)
    return jsonify({'message': 'Account created'})


@app.route("/accounts/<int:id>",  methods=["DELETE"])
def remove_account(id):
    delete_account(id)
    return jsonify({'message': 'Account deleted'})


@app.route("/transactions", methods=["GET"])
def get_transactions():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM transactions").fetchall()
    con.close()
    return jsonify([dict(row) for row in rows])


@app.route("/transactions", methods=["POST"])
def create_transactions():
    data = request.json
    account_id = data['account_id']
    category_id = data['category_id']
    amount = data['amount']
    type = data['type']
    description = data['description']
    date = data.get('date')
    add_transaction(account_id, category_id, amount, type, description, date)
    return jsonify({'message': 'Transaction created'})


@app.route("/transactions/<int:id>", methods=["DELETE"])
def remove_transactions(id):
    delete_transaction(id)
    return jsonify({'message': 'Transaction deleted'})


@app.route("/categories", methods=["GET"])
def get_categories():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM categories").fetchall()
    con.close()
    return jsonify([dict(row) for row in rows])


@app.route("/categories", methods=["POST"])
def create_categories():
    data = request.json
    name = data['name']
    type = data['type']
    add_category(name, type)
    return jsonify({'message': 'Category created'})


@app.route("/budgets", methods=["GET"])
def get_budgets():
    con = get_connection()
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM budgets").fetchall()
    con.close()
    return jsonify([dict(row) for row in rows])


@app.route("/budgets", methods=["POST"])
def create_budgets():
    data = request.json
    category_id = data['category_id']
    limit_amount = data['limit_amount']
    month = data['month']
    set_budget(category_id, limit_amount, month)
    return jsonify({'message': 'Budget created'})


@app.route("/reports/summary", methods=["GET"])
def get_summary():
    month = request.args.get("month")
    data = monthly_summary(month)
    return jsonify(data)


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
